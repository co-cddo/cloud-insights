# AWS CLI Client

Grant access to AWS billing controls and account and organization information via the AWS CLI.

``` sh

aws iam create-policy --policy-name central-aws-overview-policy \
  --policy-document file://../client_policy.json \
  --tags "Reference=https://github.com/OllieJC/central-aws-overview"

aws iam create-role --role-name central-aws-overview-role \
  --assume-role-policy-document file://../client_trust_policy.json \
  --tags "Reference=https://github.com/OllieJC/central-aws-overview"

attach-role-policy --role-name central-aws-overview-role \
  --policy-arn arn:aws:iam::ACCOUNT_ID:policy/central-aws-overview-policy

```
