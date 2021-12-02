# CDDO Cloud Insights

This is a tool to gather and interpret cost and usage data from cloud environments.

![status: proof of concept](https://img.shields.io/badge/status-proof%20of%20concept-orange)

## How it works?

### AWS

A central account polls AWS _Organizations_ that have a role and policy configured, using a central Lambda to get information about AWS usage.

#### How to configure the role?

You'll have to add at least the [client_policy_base](client_terraform/client_policy_base.json) and role to your main AWS billing account. The role allows a central role and Lambda to assume it and query organisation, cost and usage data. You can find out more about the policy permissions in this breakdown here: [policy_breakdown_base.md](policy_breakdown_base.md)

There's an additional policy ([client_policy_s3_storage_lens](client_terraform/client_policy_s3_storage_lens.json)) for configuring S3 Storage Lens automatically. This is not enabled by default and there are separate commands and steps listed in the clients. You can find out more about the policy permissions in this breakdown here: [policy_breakdown_s3_storage_lens.md](policy_breakdown_s3_storage_lens.md)

Use one of the following _methods_ to create the required role in your AWS _Organization_ main account:

- [client_terraform](client_terraform/)
- [client_cli](client_cli/)
- [client_console](client_console/)
- [client_cloudformation](client_cloudformation/)

You'll need to let us know the account number after you've configured the role and policy so we can configure the polling tool to scan your account.
