# CDDO Cloud Insights

This is a tool to gather and interpret cost and usage data from cloud environments.

![status: proof of concept](https://img.shields.io/badge/status-proof%20of%20concept-orange)

## How it works?

For AWS, you'll have to add a [policy](client_policy.json) and role to the main AWS billing account. The role allows a central role and Lambda to assume it and query organisation, cost and usage data.

You'll need to let us know the account number after you've configured the role and policy so we can configure the polling tool to scan your account.
