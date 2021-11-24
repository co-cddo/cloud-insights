import json
import boto3
import botocore.exceptions
from datetime import datetime, timedelta


def lambda_handler(event, context):
  
    # TODO:
    # - consume event/input with list of account IDs
    # - attempt to assume role in each account
    # - get details from each account use its role
    # - save results somewhere (S3 initially)
    
    current_account = getCurrentAccountDetails("123")
    org = getOrganisation()
    orgs = getChildOrganisations()
    
    day = getCostsAndUsage("day")
    cmonth = getCostsAndUsage("current-month")
    
    jsonBody = {
        "currentAccount": current_account["reason"] if "reason" in current_account else current_account,
        "organization": org["reason"] if "reason" in org else org,
        "organizations": orgs["reason"] if "reason" in orgs else orgs,
        "costsAndUsage-day": day,
        "costsAndUsage-current-month": cmonth
    }
    
    jsonBodyString = json.dumps(jsonBody, indent=2, default=str)
    print(jsonBodyString)
    return {
        'statusCode': 200,
        'body': jsonBodyString
    }


def getCurrentAccountDetails(accountId):
    res = {}
    client = boto3.client('organizations')
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


def getOrganisation():
    res = {}
    client = boto3.client('organizations')
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


def getChildOrganisations():
    res = {}
    client = boto3.client('organizations')
    try:
        res = client.list_accounts()
        if "Accounts" in res:
            return res["Accounts"]
    except client.exceptions.AWSOrganizationsNotInUseException as e:
        res = {"reason": "not-in-use"}
    except client.exceptions.AccessDeniedException as e:
        res = {"reason": "access-denied"}
    except BaseException as e:
        raise e
    return res


def getCostsAndUsage(dateRangeType):
    client = boto3.client('ce')
    
    dateFormat = "%Y-%m-%d"
    
    now = datetime.now()
    
    if dateRangeType == "day":
        yesterday = now - timedelta(days=1)
        startDate = yesterday.strftime(dateFormat)
    elif dateRangeType == "current-month":
        startDate = now.strftime("%Y-%m-01")
    
    endDate = now.strftime(dateFormat)
    
    granularity = "DAILY"
    if "month" in dateRangeType:
        granularity = "MONTHLY"
    
    res = client.get_cost_and_usage(
        TimePeriod={
            'Start': startDate,
            'End': endDate
        },
        Granularity=granularity,
        GroupBy=[
            {
                'Type': 'DIMENSION',
                'Key': 'LINKED_ACCOUNT'
            },
        ],
        Metrics=["AmortizedCost","BlendedCost","NormalizedUsageAmount"]
    )
    if "ResultsByTime" in res and "DimensionValueAttributes" in res:
        return {
            "ResultsByTime": res["ResultsByTime"],
            "DimensionValueAttributes": res["DimensionValueAttributes"]
        }
    return {}
