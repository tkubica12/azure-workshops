# IaaS managed in cloud-native way

Notes:
- Image builder to create company images
- Extension to configure and hydrate VM
- Passing information - metadata, Key Vault etc.
- VMSS, health monitor and upgrade procedures


Check scheduled events:

```bash
curl -s -H "Metadata:true" "http://169.254.169.254/metadata/scheduledevents?api-version=2019-01-01" | jq

eventId=$(curl -s -H "Metadata:true" "http://169.254.169.254/metadata/scheduledevents?api-version=2019-01-01" | jq  --raw-output .Events[0].EventId)
curl v -X POST -s -H "Metadata:true" "http://169.254.169.254/metadata/scheduledevents?api-version=2019-01-01" -d "{
	\"StartRequests\" : [
		{
			\"EventId\": \"$eventId\"
		}
	]
}"
```