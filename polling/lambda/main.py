import json
import boto3
import botocore.exceptions
import os
from datetime import datetime, timedelta
from time import time
from csv_generator import object_to_lines


PRIVATE_BUCKET = os.getenv("PRIVATE_BUCKET")
DEBUG = True if str(os.getenv("DEBUG", "f")).lower()[:1] in ["t", "1"] else False


def lambda_handler(event, context):

    stsClient = boto3.client("sts")
    stsResponse = stsClient.get_caller_identity()
    pollingAccountId = stsResponse["Account"]

    accountResults = []

    for account in get_accounts_from_s3():
        accountResult = {
            "accountId": account["accountId"],
            "assumeRoleSuccess": False,
            "assumeRoleFailureMessage": None,
        }

        credentials = {}
        try:
            roleSuffix = account["roleSuffix"] if "roleSuffix" in account else ""
            credentials = assume_role(
                pollingAccountId, account["accountId"], roleSuffix
            )
        except Exception as e:
            accountResult["assumeRoleFailureMessage"] = str(e)

        if "AccountId" in credentials:

            org_client = return_client("organizations", credentials)
            acc_client = return_client("account", credentials)

            current_account = get_current_account_details(
                org_client, credentials["AccountId"]
            )
            org = get_organisation(org_client)
            orgs = get_child_organisations(org_client, acc_client)

            iam_client = return_client("iam", credentials)
            account_summary = get_iam_summary(iam_client)
            password_policy = get_iam_password_policy(iam_client)

            ce_client = return_client("ce", credentials)
            cday = get_costs_and_usage(ce_client)
            cmonth = get_costs_and_usage(ce_client, "current-month")
            lmonth = get_costs_and_usage(ce_client, "last-month")
            lyear = get_costs_and_usage(ce_client, "last-year")
            rsizing = get_rightsizing_recommendations(ce_client)

            accountResult.update(
                {
                    "assumeRoleSuccess": True,
                    "currentAccount": current_account["reason"]
                    if "reason" in current_account
                    else current_account,
                    "organization": org["reason"] if "reason" in org else org,
                    "childAccounts": orgs["reason"]
                    if "reason" in orgs
                    else orgs["accounts"],
                    "accountSummary": account_summary,
                    "passwordPolicy": password_policy,
                    "costsAndUsage-day": cday,
                    "costsAndUsage-current-month": cmonth,
                    "costsAndUsage-last-month": lmonth,
                    "costsAndUsage-last-year": lyear,
                    "rightsizing-recommendations": rsizing,
                }
            )

        accountResults.append(accountResult)

    # print(json.dumps(accountResults, default=str))
    save_file_to_s3(
        json.dumps(accountResults, default=str, indent=2),
        "ACCOUNTRESULTS_JSON",
        pollingAccountId,
        "json",
    )

    for x in ["ORGANISATION", "ACCOUNT_DETAILS", "ACCOUNT_COSTUSAGE"]:
        save_file_to_s3(object_to_lines(accountResults, x), x, pollingAccountId)

    return {"statusCode": 200, "body": "OK"}


def get_accounts_from_s3() -> dict:
    client = boto3.client("s3")
    obj = client.get_object(Bucket=PRIVATE_BUCKET, Key="configuration/accounts.json")
    return json.loads(obj["Body"].read())


def save_file_to_s3(
    contents: str, key_type: str, pollingAccountId: str, extension: str = "csv"
):
    client = boto3.client("s3")

    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    key = f"lambda-results/{year}/{month}/{day}/{key_type}-{pollingAccountId}-{int(time())}.{extension}"

    client.put_object(
        Body=contents.encode("utf-8"),
        Bucket=PRIVATE_BUCKET,
        Key=key,
    )


def assume_role(pollingAccountId: str, accountId: str, roleSuffix: str = "") -> dict:
    client = boto3.client("sts")

    roleArn = f"arn:aws:iam::{accountId}:role/co-cddo-cloud-insights-role{roleSuffix}"
    roleSessionName = f"co-cddo-cloud-insights-lambda-{pollingAccountId}-{int(time())}"

    response = client.assume_role(
        RoleArn=roleArn, RoleSessionName=roleSessionName, DurationSeconds=900
    )

    res = {}
    if "Credentials" in response:
        res = response
        res["AccountId"] = accountId

    return res


def return_client(service: str, credentials: dict):
    client = boto3.client(
        service,
        aws_access_key_id=credentials["Credentials"]["AccessKeyId"],
        aws_secret_access_key=credentials["Credentials"]["SecretAccessKey"],
        aws_session_token=credentials["Credentials"]["SessionToken"],
    )
    return client


def get_current_account_details(client, accountId: str) -> dict:
    res = {}
    try:
        res = client.describe_account(AccountId=accountId)
        if "Account" in res:
            return res["Account"]
    except client.exceptions.AWSOrganizationsNotInUseException as e:
        res = {"reason": "not-in-use"}
    except client.exceptions.AccessDeniedException as e:
        res = {"reason": "access-denied"}
    except BaseException as e:
        raise e
    return res


def get_alternative_contacts(client, accountId: str) -> dict:
    res = {}
    try:
        res = client.GetAlternateContact(AccountId=accountId)
        if "Account" in res:
            return res["Account"]
    except client.exceptions.AWSOrganizationsNotInUseException as e:
        res = {"reason": "not-in-use"}
    except client.exceptions.AccessDeniedException as e:
        res = {"reason": "access-denied"}
    except BaseException as e:
        raise e
    return res


def get_iam_summary(client) -> dict:
    res = {}
    try:
        res = client.get_account_summary()
        if "SummaryMap" in res:
            return res["SummaryMap"]
    except Exception as e:
        if DEBUG:
            print(f"get_iam_summary: {e}")
    return res


def get_iam_password_policy(client) -> dict:
    res = {}
    try:
        res = client.get_account_password_policy()
        if "PasswordPolicy" in res:
            return res["PasswordPolicy"]
    except client.exceptions.NoSuchEntityException as e:
        res = {"reason": "not-set"}
    except Exception as e:
        if DEBUG:
            print(f"get_iam_password_policy: {e}")
    return res


def get_organisation(client) -> dict:
    res = {}
    try:
        res = client.describe_organization()
        if "Organization" in res:
            return res["Organization"]
    except client.exceptions.AWSOrganizationsNotInUseException as e:
        res = {"reason": "not-in-use"}
    except client.exceptions.AccessDeniedException as e:
        res = {"reason": "access-denied"}
    except BaseException as e:
        raise e
    return res


def get_child_organisations(client, acc_client) -> dict:
    res = {"accounts": []}
    try:
        paginator = client.get_paginator("list_accounts")
        for response in paginator.paginate():
            if "Accounts" not in response:
                continue
            items = response["Accounts"]
            for item in items:
                item["Tags"] = {}
                try:
                    tags_response = client.list_tags_for_resource(ResourceId=item["Id"])
                    if tags_response:
                        for tag in tags_response["Tags"]:
                            item["Tags"][tag["Key"]] = tag["Value"]
                except Exception as e:
                    if DEBUG:
                        print(
                            f"get_child_organisations: could not get tags for {item['Id']}"
                        )
                for ac in ["BILLING", "OPERATIONS", "SECURITY"]:
                    try:
                        ac_response = acc_client.get_alternate_contact(
                            AlternateContactType=ac, AccountId=item["Id"]
                        )
                        if ac_response and "AlternateContact" in ac_response:
                            item[f"AlternateContact-{ac}"] = ac_response[
                                "AlternateContact"
                            ]
                    except Exception as e:
                        if DEBUG:
                            print(
                                f"get_child_organisations: could not get {ac} alternate contact {item['Id']}"
                            )

                res["accounts"].append(item)

    except client.exceptions.AWSOrganizationsNotInUseException as e:
        res.update({"reason": "organizations-not-in-use"})
    except client.exceptions.AccessDeniedException as e:
        res.update({"reason": "access-denied"})
    except BaseException as e:
        raise e
    return res


def get_rightsizing_recommendations(client):
    res = {}
    try:
        response = client.get_rightsizing_recommendation(Service="AmazonEC2")
        res = {
            "Summary": response["Summary"],
            "RightsizingRecommendations": response["RightsizingRecommendations"],
        }
        if "TotalRecommendationCount" in response["Summary"]:
            response["Summary"]["TotalRecommendationCount"] = int(
                res["Summary"]["TotalRecommendationCount"]
            )
        if "EstimatedTotalMonthlySavingsAmount" in response["Summary"]:
            response["Summary"]["EstimatedTotalMonthlySavingsAmount"] = float(
                res["Summary"]["EstimatedTotalMonthlySavingsAmount"]
            )

        while "NextPageToken" in response and response["NextPageToken"]:
            response = client.get_rightsizing_recommendation(
                Service="AmazonEC2", NextPageToken=response["NextPageToken"]
            )
            if "TotalRecommendationCount" in response["Summary"]:
                res["Summary"]["TotalRecommendationCount"] += int(
                    res["Summary"]["TotalRecommendationCount"]
                )
            if "EstimatedTotalMonthlySavingsAmount" in response["Summary"]:
                res["Summary"]["EstimatedTotalMonthlySavingsAmount"] += float(
                    res["Summary"]["EstimatedTotalMonthlySavingsAmount"]
                )
            res["RightsizingRecommendations"].extend(
                response["RightsizingRecommendations"]
            )

        byAccount = {}
        for rr in res["RightsizingRecommendations"]:
            aid = rr["AccountId"]
            if aid not in byAccount:
                byAccount[aid] = {
                    "CountTotal": 0,
                    "EstimatedMonthlySavingsTotal": 0,
                    "ModifyCount": 0,
                    "TerminateCount": 0,
                    "CurrencyCode": "",
                }

            byAccount[aid]["CountTotal"] += 1

            if "ModifyRecommendationDetail" in rr:
                if "TargetInstances" in rr["ModifyRecommendationDetail"]:
                    for ti in rr["ModifyRecommendationDetail"]["TargetInstances"]:
                        if "EstimatedMonthlySavings" in ti:
                            byAccount[aid]["EstimatedMonthlySavingsTotal"] += float(
                                ti["EstimatedMonthlySavings"]
                            )
                        if "CurrencyCode" in ti:
                            byAccount[aid]["CurrencyCode"] = ti["CurrencyCode"]

            if "TerminateRecommendationDetail" in rr:
                if "EstimatedMonthlySavings" in rr["TerminateRecommendationDetail"]:
                    byAccount[aid]["EstimatedMonthlySavingsTotal"] += float(
                        rr["TerminateRecommendationDetail"]["EstimatedMonthlySavings"]
                    )
                    byAccount[aid]["CurrencyCode"] = rr[
                        "TerminateRecommendationDetail"
                    ]["CurrencyCode"]

            rrTypeCount = f'Count{rr["RightsizingType"]}'
            if rrTypeCount in byAccount[aid]:
                byAccount[aid][rrTypeCount] += 1
            else:
                byAccount[aid][rrTypeCount] = 1

        res["ByAccount"] = byAccount

    except botocore.exceptions.ClientError as e:
        res.update({"reason": "access-denied"})
    except BaseException as e:
        raise e
    return res


def get_costs_and_usage(client, dateRangeType: str = "day"):
    now = datetime.now()
    endDate = now.strftime("%Y-%m-%d")  # today's date

    if dateRangeType == "day":
        yesterday = now - timedelta(days=1)
        startDate = yesterday.strftime("%Y-%m-%d")

    elif dateRangeType == "current-month":
        startDate = now.strftime("%Y-%m-01")

    elif dateRangeType == "last-month":
        # if 2021-12-01, minus 2 days is 2021-11-30, format as 2021-11-01
        # if 2021-11-15, minus 16 days is 2021-10-31, format as 2021-10-01
        startDate = (now - timedelta(days=now.day + 1)).strftime("%Y-%m-01")
        endDate = now.strftime("%Y-%m-01")  # current month

    elif dateRangeType == "last-year":
        startDate = now.strftime(f"{now.year-1}-%m-01")
        endDate = now.strftime("%Y-%m-01")

    granularity = "MONTHLY"
    if "day" in dateRangeType:
        granularity = "DAILY"

    res = {}
    response = client.get_cost_and_usage(
        TimePeriod={"Start": startDate, "End": endDate},
        Granularity=granularity,
        GroupBy=[
            {"Type": "DIMENSION", "Key": "LINKED_ACCOUNT"},
        ],
        Metrics=["BlendedCost"],
    )
    if "ResultsByTime" in response and "DimensionValueAttributes" in response:
        res["ResultsByTime"] = response["ResultsByTime"]
        res["DimensionValueAttributes"] = response["DimensionValueAttributes"]

        while "NextPageToken" in response and response["NextPageToken"]:
            while_response = client.get_cost_and_usage(
                TimePeriod={"Start": startDate, "End": endDate},
                Granularity=granularity,
                GroupBy=[
                    {"Type": "DIMENSION", "Key": "LINKED_ACCOUNT"},
                ],
                Metrics=["BlendedCost"],
            )
            if (
                "ResultsByTime" in while_response
                and "DimensionValueAttributes" in while_response
            ):
                res["ResultsByTime"].extend(while_response["ResultsByTime"])
                res["DimensionValueAttributes"].extend(
                    while_response["DimensionValueAttributes"]
                )

    accounts = {}

    if "ResultsByTime" in res:
        cau_rbt = res["ResultsByTime"]
        total_periods = len(cau_rbt)
        for cr in range(total_periods):
            for rbt in cau_rbt[cr]["Groups"]:

                cauAId = rbt["Keys"][0]
                if cauAId not in accounts:
                    accounts[cauAId] = {}

                ak = f"costsAndUsage-BlendedCost-{dateRangeType}"
                if f"{ak}-amount" not in accounts[cauAId]:
                    amount = float(rbt["Metrics"]["BlendedCost"]["Amount"])
                    accounts[cauAId][f"{ak}-amount"] = amount
                    accounts[cauAId][f"{ak}-unit"] = rbt["Metrics"]["BlendedCost"][
                        "Unit"
                    ]
                    accounts[cauAId][f"{ak}-range"] = cau_rbt[cr]["TimePeriod"]["Start"]
                else:
                    amount = float(rbt["Metrics"]["BlendedCost"]["Amount"])
                    accounts[cauAId][f"{ak}-amount"] += amount

                if cr == (total_periods - 1):
                    endDate = cau_rbt[cr]["TimePeriod"]["End"]
                    accounts[cauAId][f"{ak}-range"] += f"_{endDate}"

    if "DimensionValueAttributes" in res:
        for dva in res["DimensionValueAttributes"]:
            if dva["Value"] in accounts:
                accounts[dva["Value"]]["accountName"] = dva["Attributes"]["description"]

    return accounts
