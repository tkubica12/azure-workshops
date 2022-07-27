# Chaos engineering
## Why
- It is usualy better to invest into ability to tolerate failures than to avoid them.
- Partial failures are the hardest.
- Failure modes in distributed systems are complex and often cascading.
- Unability to tolerate fault is often introduced with regular updates.
- Software will eventually become dependant on any observable behavior, not just documented one.
- Degraded is often better than failed and when not, use circuit breaker.
- Proper observability is key and you need actual failures to learn how to use your monitoring tools.
## vs. DR drill and testing
- DR drill is focused more on known scenarios that involve some process and human part.
- Testing is focused more on known scenarios that should pass or fail (can we meet performance minimum with one node failed?).
- Chaos engineering is focused on getting new insights. If you already know what is wrong, just fix it.
## What-if
- If something breaks, do we capture it in monitoring/alerting?
- What if this or that resource goes down?
- What if resource is overloaded (CPU, RAM)?
- What if network get latency, lower bandwidth, failures or gets partitioned?
- What if DNS starts to give wrong answers?
- What if API responds, but is sending nonsense?
- What if another failure happens when we are still recovering from first one?
## How
- Observability is important - use Azure Monitor with App Insights.
- Unless you do chaos in production simulate load with Azure Load Testing service.
- Use Azure Chaos Studio to do and orchestrate chaos experiments in SECURE WAY
 (you do not want your chaos solution to be great attack vector)
- Make sure this is continuous, not one shot (integrate to GitHub Actions)
- Envision running this in production, you should make people scared.
