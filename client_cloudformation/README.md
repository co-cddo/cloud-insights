# CloudFormation Client

Grant access to AWS billing controls and account and organization information via this CloudFormation module.

Module also available from S3: ...

### yaml

``` yaml
Transform:
  Name: 'AWS::Include'
  Parameters:
    Location: 's3://TBD/client_cloudformation/client_cloudformation_0_1.yaml'
```

### json

``` json
{
   "Transform" : {
       "Name" : "AWS::Include",
       "Parameters" : {
           "Location" : "s3://TBD/client_cloudformation/client_cloudformation_0_1.yaml"
        }
    }
}
```
