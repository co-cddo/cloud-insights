# AWS CLI Client

Grant access to AWS billing controls and account and organization information via the AWS CLI.

``` sh
# clone the repo and change directory to client_cli before running these commands
git clone https://github.com/co-cddo/cloud-insights.git
cd cloud-insights/client_cli/

# On Windows (or PowerShell) use backticks ` instead of the backslashes
aws iam create-policy --policy-name co-cddo-cloud-insights-policy \
--policy-document file://../client_terraform/client_policy.json \
--tags 'Key="Reference",Value="https://github.com/co-cddo/cloud-insights"' 'Key="Service",Value="Cabinet Office CDDO Cloud Insights Access"'

aws iam create-role --role-name co-cddo-cloud-insights-role \
--assume-role-policy-document file://../client_terraform/client_trust_policy.json \
--tags 'Key="Reference",Value="https://github.com/co-cddo/cloud-insights"' 'Key="Service",Value="Cabinet Office CDDO Cloud Insights Access"'

# Where ACCOUNT_ID is the current account (aws sts get-caller-identity)
aws iam attach-role-policy --role-name co-cddo-cloud-insights-role \
--policy-arn "arn:aws:iam::ACCOUNT_ID:policy/cddo-cloud-insights-policy"

```
