# Hosting application - WebApp + DB

1. Create WebApp using .NET Core 3.1 runtime and Windows host on new plan with P1v2 and comment on zone redundancy
2. Click on listed URL to see your web running
3. Go to App Service Editor and create new file (using right click) named default.aspx with following code:

```
I am alive! <%=System.Environment.MachineName %>
```

4. Refresh web page to see new version of your app
5. Go to Scale out, increase number of nodes and see how traffic is balanced (using curl command as browser might be caching). Also check option around autoscaling.
6. Go to Deployment slots and create new slot called staging
7. Click on staging slot, go to App Service Editor and create new file (using right click) named default.aspx with following code:

```
VERSION 2 <%=System.Environment.MachineName %>
```

8. Go to this slot app URL and see new version is there (you have just performed A/B testing as you can see old and new version side by side)
9. Go back to main app and change percentage of traffic between slots from 100/0 to 80/20. Using curl you will see that about every fifth user (based on cookie affinity) will get new version (you have just performed canary release)
10. Click on swap slots to release version 2 to production for everyone (you have just performed green/blue deployment)
11. Add Azure SQL in serverless tier (both SQL and AAD login)
12. Demonstrate how tier and performance can be changed later
13. Demonstrate geo replicas
14. Demonstrate point-in-time restore
15. Login via Query editor using AAD

# Low-code
1. On DB comment on Power Platform components
2. Click on PowerBI, download file and open it in PowerBI desktop, Connect with Microsoft Account (not Windows account)
3. Add Customer data, create table with company and name. Add multi-row card with other details on clicked customer
4. Click on Power Apps, Get Started (but do not finish wizard due to limitations in our internal tenant)
5. Open make.powerapps.com and connect Azure SQL
6. Modify app by changing title and remove password fields from detail and edit screen, click play to test
7. Go to AI Builder and Detect custom objects -> common objects -> donkey and sheep
8. Go back to DB and click Powert Automate and select Track new OneDrive files in SQL
9. In SQL create new table ```CREATE TABLE demo (filename varchar(255));```
10. Build your flow - look on Customers folder and fill demo table
11. Monitor executions and then go to database an ```SELECT * from demo```

# Event based architectures with serverless and data streaming
1. Create Azure Function App with Node.js and Windows host and Application Insights enabled.
2. Create Storage Account and container "outcontainer"
3. Create Event Hub namespace and hub
4. Create Function with shttp trigger
5. Open Monitor page, go to storage account and create message - see logs
6. Modify Integrations to include output binding to write files to blob storage and to eventhub
7. Modify code and test

```javascript
module.exports = async function (context, req) {
    context.log("Executing...");
    const temperature = (req.query.temperature || (req.body && req.body.temperature));
    context.log("{\"temperature\": " + temperature + "}");
    context.bindings.outputBlob = "{\"temperature\": " + temperature + "}";
    context.bindings.outputEventHubMessage  = "{\"temperature\": " + temperature + "}";
    context.done();
}
```

7. Call function couple of times and see blobs being created 
```curl 'https://tomaskubicadhldemo12.azurewebsites.net/api/mydemo?code=Y4yKTYs1W5wREiDN9qpd1dr5i4qcLSW0llusiuLHW-5FAzFuewm5Bg==&temperature='$RANDOM ```
8. Go to Application Insights and see application monitoring -> Application map, Transaction search, 
9. Go to event hub and click Process data to generate Stream Analytics job
```
SELECT
    *
INTO
    [OutputAlias]
FROM
    [mydata]
WHERE temperature > 20000
```
10. Open Azure Synapse studio - Manage and show SQL serverless and dedicated pools, Spark Pools, ADX pools, show Integration pipelines (Copy data -> source, then browse template)

# Automated infrastructure
https://github.com/tomas-iac
1. Deploy landing zone before presentation
2. Deploy project1 using GitHub Actions
3. Go to docs and explain strategy, modules, workflows
4. Go to Azure and showcase deployed infrastructure

# Management and edge solutions
1. Open tomaskubicaiot demo IoT Hub that has been prepared before (add IoT Device from VS Code and deploy Linux VM and register as IoT Edge device)
2. Show Devices (messaging, device twin, config) and Add new to see authentication options including certificate
3. Show IoT Edge devices and modules, click on Set modules to see marketplace and focus on cloud services such as Stream Analytics or Cognitive services
4. Showcase Arc using ArcBoc jumpstart [https://azurearcjumpstart.io/](https://azurearcjumpstart.io/)

