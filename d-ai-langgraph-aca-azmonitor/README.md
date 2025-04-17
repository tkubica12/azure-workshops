# Multi-agent Lang Graph example with UI, OpenTelemetry, Azure Monitor and Container Apps

## Monitoring
### Local Aspire dashboard
In ```.env``` file set OTEL_EXPORTER_OTLP_ENDPOINT to ```http://localhost:4317```. To access dashboard see logs from Aspire container start with URL with key.

```powershell
docker run --rm -it `
-p 18888:18888 `
-p 4317:18889 `
--name aspire-dashboard `
mcr.microsoft.com/dotnet/aspire-dashboard:latest
```

Run application and see it collecting:
- Logs from appp
- Traces that include LLM calls with input and output texts
- Metrics including autoinstrumented token counts and also custom "agent message count" metric