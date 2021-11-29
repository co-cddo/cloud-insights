# CloudFormation Client

Grant access to AWS billing controls and account and organization information via this CloudFormation module.

Module will be available from S3.

### yaml

``` yaml
Transform:
  Name: 'AWS::Include'
  Parameters:
    Location: 's3://co-cddo-cloud-insights-public-prod/client_cloudformation/client_cloudformation_0_1.yaml'
```

### json

``` json
{
   "Transform" : {
       "Name" : "AWS::Include",
       "Parameters" : {
           "Location" : "s3://co-cddo-cloud-insights-public-prod/client_cloudformation/client_cloudformation_0_1.json"
        }
    }
}
```
