# Using DAPR platform together with scale to zero serverless
In this lab we will deploy additional two components to test scale to zero and DAPR application platform. Note those components are just for our test and not required for functionality of our TODO application.

DAPR is application platform that provides APIs for developers allowing them to use patterns of distributed applications without being bounded to specific implementation. This brings true multi-cloud and hybrid deployments. We have one component event-generator that is using DAPR API to send asynchronous messages to topic and second component is event-processor that is using DAPR API to process messages.


**TBD - waiting for migration to Microsoft.App RP and central daprCompontents**


az bicep build -f main.bicep
az deployment group create -g $prefix-rg --template-file main.json --parameters $prefix.parameters.json
