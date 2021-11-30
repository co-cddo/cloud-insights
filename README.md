# CDDO Cloud Insights

This is a tool to gather and interpret cost and usage data from cloud environments.

![status: proof of concept](https://img.shields.io/badge/status-proof%20of%20concept-orange)

## How it works?

### AWS

A central account polls AWS _Organizations_ that have a role and policy configured, using a central Lambda to get information about AWS usage.

#### How to configure the role?

You'll have to add a [policy](client_terraform/client_policy.json) and role to your main AWS billing account. The role allows a central role and Lambda to assume it and query organisation, cost and usage data. You can find out more about the policy permissions in this breakdown here: [policy_breakdown.md](policy_breakdown.md)

Use one of the following _methods_ to create the required role in your AWS _Organization_ main account:

- [client_terraform](client_terraform/)
- [client_cli](client_cli/)
- [client_console](client_console/)
- [client_cloudformation](client_cloudformation/)

You'll need to let us know the account number after you've configured the role and policy so we can configure the polling tool to scan your account.
