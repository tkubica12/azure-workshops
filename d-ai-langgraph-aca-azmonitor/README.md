# Multi-agent Lang Graph example with UI, OpenTelemetry, Azure Monitor and Container Apps

## Monitoring
### Local Aspire dashboard
In ```.env``` file set OTEL_EXPORTER_OTLP_ENDPOINT to ```https://localhost:18889/v1/traces```, access dashboard at ```https://localhost:18888``` and run the app.

```powershell
docker run --rm -it `
-p 18888:18888 `
-p 4317:18889 `
--name aspire-dashboard `
mcr.microsoft.com/dotnet/aspire-dashboard:latest
```