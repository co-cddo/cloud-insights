# AWS CLI Client

Grant access to AWS billing controls and account and organization information via the AWS CLI.

``` sh

aws iam create-policy --policy-name cddo-cloud-insights-policy --policy-document file://../client_terraform/client_policy.json --tags 'Key="Reference",Value="https://github.com/co-cddo/cloud-insights"' 'Key="Service",Value="Cabinet Office CDDO Cloud Insights Access"'

aws iam create-role --role-name cddo-cloud-insights-role --assume-role-policy-document file://../client_terraform/client_trust_policy.json --tags 'Key="Reference",Value="https://github.com/co-cddo/cloud-insights"' 'Key="Service",Value="Cabinet Office CDDO Cloud Insights Access"'

aws iam attach-role-policy --role-name cddo-cloud-insights-role --policy-arn arn:aws:iam::ACCOUNT_ID:policy/cddo-cloud-insights-policy

```
