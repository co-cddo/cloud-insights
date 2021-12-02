import json

JOIN_CHAR = ","
JOIN_REPL = "%2C"

KEYS = {
    "ORGANISATION": [
        "accountId",
        "organizationAccountEmail",
        "organizationAccountCount",
        "organizationAccountMFAEnabled",
        "organizationAccountAccessKeysPresent",
        "organizationAccountPasswordPolicy",
        "rightsizing-Summary-TotalRecommendationCount",
        "rightsizing-Summary-EstimatedTotalMonthlySavingsAmount",
        "alternateContact-BILLING",
        "alternateContact-SECURITY",
        "alternateContact-OPERATIONS",
    ],
    "ACCOUNT_DETAILS": [
        "accountId",
        "accountIsOrganization",
        "organizationAccountId",
        "accountName",
        "accountStatus",
        "accountJoinedTimestamp",
        "accountEmail",
        "accountTags",
        "accountMFAEnabled",
        "accountAccessKeysPresent",
        "passwordPolicy",
        "alternateContact-BILLING",
        "alternateContact-SECURITY",
        "alternateContact-OPERATIONS",
    ],
    "ACCOUNT_COSTUSAGE": [
        "accountId",
        "accountName",
        "costsAndUsage-BlendedCost-day-amount",
        "costsAndUsage-BlendedCost-day-unit",
        "costsAndUsage-BlendedCost-day-range",
        "costsAndUsage-BlendedCost-current-month-amount",
        "costsAndUsage-BlendedCost-current-month-unit",
        "costsAndUsage-BlendedCost-current-month-range",
        "costsAndUsage-BlendedCost-last-month-amount",
        "costsAndUsage-BlendedCost-last-month-unit",
        "costsAndUsage-BlendedCost-last-month-range",
        "costsAndUsage-BlendedCost-last-year-amount",
        "costsAndUsage-BlendedCost-last-year-unit",
        "costsAndUsage-BlendedCost-last-year-range",
        "rightsizing-CountTotal",
        "rightsizing-ModifyCount",
        "rightsizing-TerminateCount",
        "rightsizing-EstimatedMonthlySavingsTotal",
    ],
}


def initial_line_dict(accountId: str, key_type: str) -> dict:
    line_res = {}
    for k in KEYS[key_type]:
        line_res[k] = ""
    line_res["accountId"] = str(accountId)
    return line_res


def simply_json_to_string(tags):
    return ";".join([f"{x}=" + str(y).replace(";", "%3B") for x, y in tags.items()])


def dict_items_to_line(items: dict) -> str:
    return JOIN_CHAR.join(
        [
            f"'{y}'"
            if y and "accountid" in x.lower()
            else str(y).replace(JOIN_CHAR, JOIN_REPL)
            for x, y in items.items()
        ]
    )


def object_to_lines(input_object: list, key_type: str) -> list:
    res = []

    accountIds = []
    accountDetails = {}
    orgIds = []
    orgDetails = {}

    for i in input_object:
        thisAccountId = i["accountId"]

        if thisAccountId not in accountIds:
            accountIds.append(i["accountId"])

        if thisAccountId not in accountDetails:
            accountDetails[thisAccountId] = {"accountIsOrganization": "no"}

            if "accountSummary" in i and i["accountSummary"]:
                accountDetails[thisAccountId]["accountMFAEnabled"] = i[
                    "accountSummary"
                ]["AccountMFAEnabled"]
                accountDetails[thisAccountId]["accountAccessKeysPresent"] = i[
                    "accountSummary"
                ]["AccountAccessKeysPresent"]

            if "passwordPolicy" in i and i["passwordPolicy"]:
                accountDetails[thisAccountId]["passwordPolicy"] = simply_json_to_string(
                    i["passwordPolicy"]
                )

        if "organization" in i and "MasterAccountId" in i["organization"]:
            o = i["organization"]["MasterAccountId"]

            if thisAccountId == o:
                accountDetails[thisAccountId]["accountIsOrganization"] = "yes"

            accountDetails[thisAccountId]["organizationAccountId"] = o

            if i["organization"]["MasterAccountId"] not in orgIds:
                orgIds.append(o)
                orgDetails[o] = {
                    "organizationAccountEmail": i["organization"]["MasterAccountEmail"]
                }

                if thisAccountId == o:
                    if "accountSummary" in i and i["accountSummary"]:
                        orgDetails[o]["organizationAccountMFAEnabled"] = i[
                            "accountSummary"
                        ]["AccountMFAEnabled"]
                        orgDetails[o]["organizationAccountAccessKeysPresent"] = i[
                            "accountSummary"
                        ]["AccountAccessKeysPresent"]

                    if "passwordPolicy" in i and i["passwordPolicy"]:
                        orgDetails[o][
                            "organizationAccountPasswordPolicy"
                        ] = simply_json_to_string(i["passwordPolicy"])

                    if (
                        "rightsizing-recommendations" in i
                        and "Summary" in i["rightsizing-recommendations"]
                    ):
                        irsrs = i["rightsizing-recommendations"]["Summary"]
                        orgDetails[o][
                            "rightsizing-Summary-TotalRecommendationCount"
                        ] = irsrs["TotalRecommendationCount"]
                        orgDetails[o][
                            "rightsizing-Summary-EstimatedTotalMonthlySavingsAmount"
                        ] = irsrs["EstimatedTotalMonthlySavingsAmount"]

                if type(i["childAccounts"]) == list:
                    orgDetails[o]["organizationAccountCount"] = len(i["childAccounts"])

                    for ca in i["childAccounts"]:
                        caId = ca["Id"]

                        if caId not in accountIds:
                            accountIds.append(caId)

                        if caId not in accountDetails:
                            accountDetails[caId] = {}

                        accountDetails[caId].update(
                            {
                                "accountName": ca["Name"],
                                "accountStatus": ca["Status"],
                                "accountJoinedTimestamp": ca["JoinedTimestamp"],
                                "accountEmail": ca["Email"],
                                "accountTags": simply_json_to_string(ca["Tags"]),
                                "accountIsOrganization": "yes" if caId == o else "no",
                                "organizationAccountId": o,
                            }
                        )

                        for ac in ["BILLING", "SECURITY", "OPERATIONS"]:
                            if f"AlternateContact-{ac}" in ca:
                                ac_res = {
                                    f"alternateContact-{ac}": simply_json_to_string(
                                        ca[f"AlternateContact-{ac}"]
                                    ),
                                }
                                if caId == o:
                                    orgDetails[o].update(ac_res)
                                accountDetails[caId].update(ac_res)

        for x in ["current-month", "day", "last-month", "last-year"]:
            cau = f"costsAndUsage-{x}"
            if cau in i:
                for a in i[cau]:
                    if a not in accountDetails:
                        accountDetails[a] = i[cau][a]
                    else:
                        accountDetails[a].update(i[cau][a])

        if (
            "rightsizing-recommendations" in i
            and "ByAccount" in i["rightsizing-recommendations"]
        ):
            irrrba = i["rightsizing-recommendations"]["ByAccount"]
            for a in irrrba:
                rrr = {
                    "rightsizing-CountTotal": irrrba["CountTotal"],
                    "rightsizing-ModifyCount": irrrba["ModifyCount"],
                    "rightsizing-TerminateCount": irrrba["TerminateCount"],
                    "rightsizing-EstimatedMonthlySavingsTotal": irrrba[
                        "EstimatedMonthlySavingsTotal"
                    ],
                }
                if a not in accountDetails:
                    accountDetails[a] = rrr
                else:
                    accountDetails[a].update(rrr)

    csvLines = [JOIN_CHAR.join(KEYS[key_type])]

    if key_type == "ORGANISATION":
        for o in orgIds:
            line_item = initial_line_dict(o, key_type)
            for od in orgDetails[o]:
                if od in line_item:
                    line_item[od] = orgDetails[o][od]
            csvLines.append(dict_items_to_line(line_item))
            # print(dict_items_to_line(line_item))

    if key_type in ["ACCOUNT_DETAILS", "ACCOUNT_COSTUSAGE"]:
        for a in accountIds:
            line_item = initial_line_dict(a, key_type)
            for ad in accountDetails[a]:
                if ad in line_item:
                    line_item[ad] = accountDetails[a][ad]
            csvLines.append(dict_items_to_line(line_item))
            # print(dict_items_to_line(line_item))

    return "\n".join(csvLines)
