# AWS CLI Client

Grant access to AWS billing controls and account and organization information via the AWS CLI.

### Bash

``` sh
# clone the repo and change directory to client_cli before the below commands
git clone https://github.com/co-cddo/cloud-insights.git
cd cloud-insights/client_cli/

aws iam create-policy --policy-name co-cddo-cloud-insights-policy \
--policy-document file://../client_terraform/client_policy.json \
--tags 'Key="Reference",Value="https://github.com/co-cddo/cloud-insights"' 'Key="Service",Value="Cabinet Office CDDO Cloud Insights Access"'

aws iam create-role --role-name co-cddo-cloud-insights-role \
--assume-role-policy-document file://../client_terraform/client_trust_policy.json \
--tags 'Key="Reference",Value="https://github.com/co-cddo/cloud-insights"' 'Key="Service",Value="Cabinet Office CDDO Cloud Insights Access"'

GCI=$(aws sts get-caller-identity | tr "\n" " " | sed 's/.*Account\": \"\([[:digit:]]*\)\".*/\1/') # yes, jq is a thing
aws iam attach-role-policy --role-name co-cddo-cloud-insights-role \
--policy-arn "arn:aws:iam::$GCI:policy/co-cddo-cloud-insights-policy"

```

### PowerShell

``` PowerShell
# clone the repo and change directory to client_cli before the below commands
git clone https://github.com/co-cddo/cloud-insights.git
cd cloud-insights/client_cli/

aws iam create-policy --policy-name co-cddo-cloud-insights-policy `
--policy-document file://../client_terraform/client_policy.json `
--tags 'Key="Reference",Value="https://github.com/co-cddo/cloud-insights"' 'Key="Service",Value="Cabinet Office CDDO Cloud Insights Access"'

aws iam create-role --role-name co-cddo-cloud-insights-role `
--assume-role-policy-document file://../client_terraform/client_trust_policy.json `
--tags 'Key="Reference",Value="https://github.com/co-cddo/cloud-insights"' 'Key="Service",Value="Cabinet Office CDDO Cloud Insights Access"'

$GCI=(aws sts get-caller-identity | ConvertFrom-Json)
aws iam attach-role-policy --role-name co-cddo-cloud-insights-role `
--policy-arn "arn:aws:iam::$($GCI.Account):policy/co-cddo-cloud-insights-policy"

```
