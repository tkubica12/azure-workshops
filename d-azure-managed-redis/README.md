# Azure Managed Redis demo
Use Terraform to deploy Azure Managed Redis in different configurations:
- OSS cluster
- Enterprise cluster
- Enterprise cluster with geo-replication

It also deploy demo scripts in Azure Container apps for each scenario. Python code is stored in image so you can jump into container and execute it manually. (TBD)

## Scenarios

| test | description | Entertprise cluster | OSS cluster | active-active geo enterprise cluster |
| --- | --- | --- | --- | --- |
| basic_test | Simply connects and reads a key | ✅ | ✅ | ✅ |
| json_test | Showcase storing JSON and quering by its components | ✅ | ❌ | ✅ |
| sharding_test | Tests cross-shard multi-key read and write to cluster (MSET, MGET) | ✅ | ❌ | ⚠️ (MGET yes, MSET no) |
| search_test | Tests search capabilities for full-text and vector search using OpenAI embeddings | ✅ | ❌ | ✅ |
| latency_test | Tests latency of read and write operations | ✅ | ✅ | ✅ |