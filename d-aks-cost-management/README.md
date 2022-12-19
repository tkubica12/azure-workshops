# Using tagging and Opencost to allocate costs to clusters, namespaces and individual services
This demo show how to use resource tags on cluster resources, nodepools and object created via Kubernetes API such as disks for Volume or Public IPs for Services. This is tag structure:
- L1=AKS01 -> the same for every resource in cluster so can filter based on this in Azure Cost Management
- L2 tags -> you can use those to group by in Azure Cost Management
  - L2=AKS01-SHARED -> cluster itself including LB and Public IP, default nodepool as system nodepool
  - L2=AKS01-T01 -> Resources for Team01 - nodepool, disks, services
  - L2=AKS01-T02 -> Resources for Team02 - nodepool, disks, services

Then you can use allocation feature to showcase mapping of shared costs to teams -> allocate AKS01-SHARED tag to tags AKS01-T01 and AKS01-T02 eg. based on compute usage ratio.

For next level of granularity (namespaces within the same nodepool) this demo installs OpenCost project.

## Deploy

```bash
# Deploy Terraform including Helm carts
cd terraform
terraform apply -auto-approve
```

## Use OpenCost API
Replace with your public IP on opencost service (see Service in your AKS cluster).

```bash
curl http://20.31.220.228:9090/allocation/compute \
  -d window=1d \
  -d step=1d \
  -d resolution=10m \
  -d aggregate=namespace \
  -d accumulate=false \
  -G | jq
```

```json
{
  "code": 200,
  "status": "success",
  "data": [
    {},
    {},
    {
      "a-a": {
        "name": "a-a",
        "properties": {
          "cluster": "L1-A",
          "node": "aks-pool1-13761008-vmss000000",
          "container": "nginx",
          "controllerKind": "deployment",
          "namespace": "a-a",
          "providerID": "azure:///subscriptions/d3b7888f-c26e-4961-a976-ff9d5b31dfd3/resourceGroups/mc_d-kubecost_d-kubecost_westeurope/providers/Microsoft.Compute/virtualMachineScaleSets/aks-pool1-13761008-vmss/virtualMachines/0"
        },
        "window": {
          "start": "2022-12-16T13:55:23Z",
          "end": "2022-12-19T13:55:23Z"
        },
        "start": "2022-12-19T08:30:00Z",
        "end": "2022-12-19T13:50:00Z",
        "minutes": 320,
        "cpuCores": 0.3,
        "cpuCoreRequestAverage": 0.3,
        "cpuCoreUsageAverage": 0,
        "cpuCoreHours": 1.6,
        "cpuCost": 0.0624,
        "cpuCostAdjustment": 0,
        "cpuEfficiency": 0,
        "gpuCount": 0,
        "gpuHours": 0,
        "gpuCost": 0,
        "gpuCostAdjustment": 0,
        "networkTransferBytes": 0,
        "networkReceiveBytes": 0,
        "networkCost": 0,
        "networkCostAdjustment": 0,
        "loadBalancerCost": 0,
        "loadBalancerCostAdjustment": 0,
        "pvBytes": 16696685363.2,
        "pvByteHours": 89048988603.73334,
        "pvCost": 0.004544,
        "pvs": null,
        "pvCostAdjustment": 0,
        "ramBytes": 167772160,
        "ramByteRequestAverage": 167772160,
        "ramByteUsageAverage": 13955072,
        "ramByteHours": 894784853.333333,
        "ramCost": 0.001597,
        "ramCostAdjustment": 0,
        "ramEfficiency": 0.083179,
        "sharedCost": 0,
        "externalCost": 0,
        "totalCost": 0.068542,
        "totalEfficiency": 0.002076,
        "rawAllocationOnly": null
      },
      "a-b": {
        "name": "a-b",
        "properties": {
          "cluster": "L1-A",
          "node": "aks-pool1-13761008-vmss000000",
          "container": "nginx",
          "controllerKind": "deployment",
          "namespace": "a-b",
          "providerID": "azure:///subscriptions/d3b7888f-c26e-4961-a976-ff9d5b31dfd3/resourceGroups/mc_d-kubecost_d-kubecost_westeurope/providers/Microsoft.Compute/virtualMachineScaleSets/aks-pool1-13761008-vmss/virtualMachines/0"
        },
        "window": {
          "start": "2022-12-16T13:55:23Z",
          "end": "2022-12-19T13:55:23Z"
        },
        "start": "2022-12-19T08:30:00Z",
        "end": "2022-12-19T13:50:00Z",
        "minutes": 320,
        "cpuCores": 0.65,
        "cpuCoreRequestAverage": 0.65,
        "cpuCoreUsageAverage": 0,
        "cpuCoreHours": 3.466667,
        "cpuCost": 0.1352,
        "cpuCostAdjustment": 0,
        "cpuEfficiency": 0,
        "gpuCount": 0,
        "gpuHours": 0,
        "gpuCost": 0,
        "gpuCostAdjustment": 0,
        "networkTransferBytes": 0,
        "networkReceiveBytes": 0,
        "networkCost": 0,
        "networkCostAdjustment": 0,
        "loadBalancerCost": 0,
        "loadBalancerCostAdjustment": 0,
        "pvBytes": 8348342681.6,
        "pvByteHours": 44524494301.86667,
        "pvCost": 0.002272,
        "pvs": null,
        "pvCostAdjustment": 0,
        "ramBytes": 436207616,
        "ramByteRequestAverage": 436207616,
        "ramByteUsageAverage": 17489920,
        "ramByteHours": 2326440618.666667,
        "ramCost": 0.004154,
        "ramCostAdjustment": 0,
        "ramEfficiency": 0.040095,
        "sharedCost": 0,
        "externalCost": 0,
        "totalCost": 0.141626,
        "totalEfficiency": 0.001195,
        "rawAllocationOnly": null
      },
      "b-a": {
        "name": "b-a",
        "properties": {
          "cluster": "L1-A",
          "node": "aks-pool2-22716520-vmss000000",
          "container": "nginx",
          "controllerKind": "deployment",
          "namespace": "b-a",
          "providerID": "azure:///subscriptions/d3b7888f-c26e-4961-a976-ff9d5b31dfd3/resourceGroups/mc_d-kubecost_d-kubecost_westeurope/providers/Microsoft.Compute/virtualMachineScaleSets/aks-pool2-22716520-vmss/virtualMachines/0"
        },
        "window": {
          "start": "2022-12-16T13:55:23Z",
          "end": "2022-12-19T13:55:23Z"
        },
        "start": "2022-12-19T08:30:00Z",
        "end": "2022-12-19T13:50:00Z",
        "minutes": 320,
        "cpuCores": 0.85,
        "cpuCoreRequestAverage": 0.85,
        "cpuCoreUsageAverage": 0,
        "cpuCoreHours": 4.533333,
        "cpuCost": 0.1768,
        "cpuCostAdjustment": 0,
        "cpuEfficiency": 0,
        "gpuCount": 0,
        "gpuHours": 0,
        "gpuCost": 0,
        "gpuCostAdjustment": 0,
        "networkTransferBytes": 0,
        "networkReceiveBytes": 0,
        "networkCost": 0,
        "networkCostAdjustment": 0,
        "loadBalancerCost": 0,
        "loadBalancerCostAdjustment": 0,
        "pvBytes": 8348342681.6,
        "pvByteHours": 44524494301.86667,
        "pvCost": 0.002272,
        "pvs": null,
        "pvCostAdjustment": 0,
        "ramBytes": 167772160,
        "ramByteRequestAverage": 167772160,
        "ramByteUsageAverage": 17498112,
        "ramByteHours": 894784853.333333,
        "ramCost": 0.001597,
        "ramCostAdjustment": 0,
        "ramEfficiency": 0.104297,
        "sharedCost": 0,
        "externalCost": 0,
        "totalCost": 0.18067,
        "totalEfficiency": 0.000934,
        "rawAllocationOnly": null
      },
      "b-b": {
        "name": "b-b",
        "properties": {
          "cluster": "L1-A",
          "node": "aks-pool2-22716520-vmss000000",
          "container": "nginx",
          "controllerKind": "deployment",
          "namespace": "b-b",
          "providerID": "azure:///subscriptions/d3b7888f-c26e-4961-a976-ff9d5b31dfd3/resourceGroups/mc_d-kubecost_d-kubecost_westeurope/providers/Microsoft.Compute/virtualMachineScaleSets/aks-pool2-22716520-vmss/virtualMachines/0"
        },
        "window": {
          "start": "2022-12-16T13:55:23Z",
          "end": "2022-12-19T13:55:23Z"
        },
        "start": "2022-12-19T08:30:00Z",
        "end": "2022-12-19T13:50:00Z",
        "minutes": 320,
        "cpuCores": 0.45,
        "cpuCoreRequestAverage": 0.45,
        "cpuCoreUsageAverage": 0,
        "cpuCoreHours": 2.4,
        "cpuCost": 0.0936,
        "cpuCostAdjustment": 0,
        "cpuEfficiency": 1e-06,
        "gpuCount": 0,
        "gpuHours": 0,
        "gpuCost": 0,
        "gpuCostAdjustment": 0,
        "networkTransferBytes": 0,
        "networkReceiveBytes": 0,
        "networkCost": 0,
        "networkCostAdjustment": 0,
        "loadBalancerCost": 0,
        "loadBalancerCostAdjustment": 0,
        "pvBytes": 33393370726.4,
        "pvByteHours": 178097977207.46667,
        "pvCost": 0.009089,
        "pvs": null,
        "pvCostAdjustment": 0,
        "ramBytes": 134217728,
        "ramByteRequestAverage": 134217728,
        "ramByteUsageAverage": 10499120.454259,
        "ramByteHours": 715827882.666667,
        "ramCost": 0.001278,
        "ramCostAdjustment": 0,
        "ramEfficiency": 0.078225,
        "sharedCost": 0,
        "externalCost": 0,
        "totalCost": 0.103967,
        "totalEfficiency": 0.001054,
        "rawAllocationOnly": null
      },
      "grafana": {
        "name": "grafana",
        "properties": {
          "cluster": "L1-A",
          "node": "aks-default-31744723-vmss000000",
          "container": "grafana",
          "controller": "grafana",
          "controllerKind": "deployment",
          "namespace": "grafana",
          "pod": "grafana-665654b46d-srk9q",
          "services": [
            "grafana"
          ],
          "providerID": "azure:///subscriptions/d3b7888f-c26e-4961-a976-ff9d5b31dfd3/resourceGroups/mc_d-kubecost_d-kubecost_westeurope/providers/Microsoft.Compute/virtualMachineScaleSets/aks-default-31744723-vmss/virtualMachines/0",
          "labels": {
            "app_kubernetes_io_instance": "grafana",
            "app_kubernetes_io_name": "grafana",
            "kubernetes_io_metadata_name": "grafana",
            "name": "grafana",
            "pod_template_hash": "665654b46d"
          }
        },
        "window": {
          "start": "2022-12-16T13:55:23Z",
          "end": "2022-12-19T13:55:23Z"
        },
        "start": "2022-12-19T08:30:00Z",
        "end": "2022-12-19T13:50:00Z",
        "minutes": 320,
        "cpuCores": 0,
        "cpuCoreRequestAverage": 0,
        "cpuCoreUsageAverage": 0.000214,
        "cpuCoreHours": 0,
        "cpuCost": 0,
        "cpuCostAdjustment": 0,
        "cpuEfficiency": 0,
        "gpuCount": 0,
        "gpuHours": 0,
        "gpuCost": 0,
        "gpuCostAdjustment": 0,
        "networkTransferBytes": 0,
        "networkReceiveBytes": 0,
        "networkCost": 0,
        "networkCostAdjustment": 0,
        "loadBalancerCost": 0.133333,
        "loadBalancerCostAdjustment": 0,
        "pvBytes": 0,
        "pvByteHours": 0,
        "pvCost": 0,
        "pvs": null,
        "pvCostAdjustment": 0,
        "ramBytes": 0,
        "ramByteRequestAverage": 0,
        "ramByteUsageAverage": 57516567.925234,
        "ramByteHours": 0,
        "ramCost": 0,
        "ramCostAdjustment": 0,
        "ramEfficiency": 0,
        "sharedCost": 0,
        "externalCost": 0,
        "totalCost": 0.133333,
        "totalEfficiency": 0,
        "rawAllocationOnly": {
          "cpuCoreUsageMax": 0.00021393253219842868,
          "ramByteUsageMax": 57782272
        }
      },
      "ingress-nginx": {
        "name": "ingress-nginx",
        "properties": {
          "cluster": "L1-A",
          "node": "aks-default-31744723-vmss000000",
          "container": "controller",
          "controller": "ingress-nginx-controller",
          "controllerKind": "deployment",
          "namespace": "ingress-nginx",
          "pod": "ingress-nginx-controller-7d5fb757db-vfrdw",
          "services": [
            "ingress-nginx-controller-admission",
            "ingress-nginx-controller"
          ],
          "providerID": "azure:///subscriptions/d3b7888f-c26e-4961-a976-ff9d5b31dfd3/resourceGroups/mc_d-kubecost_d-kubecost_westeurope/providers/Microsoft.Compute/virtualMachineScaleSets/aks-default-31744723-vmss/virtualMachines/0",
          "labels": {
            "app_kubernetes_io_component": "controller",
            "app_kubernetes_io_instance": "ingress-nginx",
            "app_kubernetes_io_name": "ingress-nginx",
            "kubernetes_io_metadata_name": "ingress-nginx",
            "name": "ingress-nginx",
            "pod_template_hash": "7d5fb757db"
          }
        },
        "window": {
          "start": "2022-12-16T13:55:23Z",
          "end": "2022-12-19T13:55:23Z"
        },
        "start": "2022-12-19T08:30:00Z",
        "end": "2022-12-19T13:50:00Z",
        "minutes": 320,
        "cpuCores": 0.1,
        "cpuCoreRequestAverage": 0.1,
        "cpuCoreUsageAverage": 0.000195,
        "cpuCoreHours": 0.533333,
        "cpuCost": 0.0208,
        "cpuCostAdjustment": 0,
        "cpuEfficiency": 0.001953,
        "gpuCount": 0,
        "gpuHours": 0,
        "gpuCost": 0,
        "gpuCostAdjustment": 0,
        "networkTransferBytes": 0,
        "networkReceiveBytes": 0,
        "networkCost": 0,
        "networkCostAdjustment": 0,
        "loadBalancerCost": 0.133333,
        "loadBalancerCostAdjustment": 0,
        "pvBytes": 0,
        "pvByteHours": 0,
        "pvCost": 0,
        "pvs": null,
        "pvCostAdjustment": 0,
        "ramBytes": 94371840,
        "ramByteRequestAverage": 94371840,
        "ramByteUsageAverage": 77395885.05919,
        "ramByteHours": 503316480,
        "ramCost": 0.000899,
        "ramCostAdjustment": 0,
        "ramEfficiency": 0.820116,
        "sharedCost": 0,
        "externalCost": 0,
        "totalCost": 0.155032,
        "totalEfficiency": 0.035835,
        "rawAllocationOnly": {
          "cpuCoreUsageMax": 0.0001953079018612351,
          "ramByteUsageMax": 81428480
        }
      },
      "kube-system": {
        "name": "kube-system",
        "properties": {
          "cluster": "L1-A",
          "namespace": "kube-system"
        },
        "window": {
          "start": "2022-12-16T13:55:23Z",
          "end": "2022-12-19T13:55:23Z"
        },
        "start": "2022-12-19T08:30:00Z",
        "end": "2022-12-19T13:50:00Z",
        "minutes": 320,
        "cpuCores": 1.588,
        "cpuCoreRequestAverage": 1.588,
        "cpuCoreUsageAverage": 0.005024,
        "cpuCoreHours": 8.469333,
        "cpuCost": 0.330304,
        "cpuCostAdjustment": 0,
        "cpuEfficiency": 0.003164,
        "gpuCount": 0,
        "gpuHours": 0,
        "gpuCost": 0,
        "gpuCostAdjustment": 0,
        "networkTransferBytes": 0,
        "networkReceiveBytes": 0,
        "networkCost": 0,
        "networkCostAdjustment": 0,
        "loadBalancerCost": 0,
        "loadBalancerCostAdjustment": 0,
        "pvBytes": 0,
        "pvByteHours": 0,
        "pvCost": 0,
        "pvs": null,
        "pvCostAdjustment": 0,
        "ramBytes": 1237319680,
        "ramByteRequestAverage": 1237319680,
        "ramByteUsageAverage": 711582979.759612,
        "ramByteHours": 6599038293.333336,
        "ramCost": 0.011782,
        "ramCostAdjustment": 0,
        "ramEfficiency": 0.5751,
        "sharedCost": 0,
        "externalCost": 0,
        "totalCost": 0.342086,
        "totalEfficiency": 0.022861,
        "rawAllocationOnly": null
      },
      "opencost": {
        "name": "opencost",
        "properties": {
          "cluster": "L1-A",
          "controller": "opencost",
          "controllerKind": "deployment",
          "namespace": "opencost"
        },
        "window": {
          "start": "2022-12-16T13:55:23Z",
          "end": "2022-12-19T13:55:23Z"
        },
        "start": "2022-12-19T08:30:00Z",
        "end": "2022-12-19T13:50:00Z",
        "minutes": 320,
        "cpuCores": 0.02,
        "cpuCoreRequestAverage": 0.02,
        "cpuCoreUsageAverage": 0.000276,
        "cpuCoreHours": 0.106667,
        "cpuCost": 0.00416,
        "cpuCostAdjustment": 0,
        "cpuEfficiency": 0.013798,
        "gpuCount": 0,
        "gpuHours": 0,
        "gpuCost": 0,
        "gpuCostAdjustment": 0,
        "networkTransferBytes": 0,
        "networkReceiveBytes": 0,
        "networkCost": 0,
        "networkCostAdjustment": 0,
        "loadBalancerCost": 0.133333,
        "loadBalancerCostAdjustment": 0,
        "pvBytes": 0,
        "pvByteHours": 0,
        "pvCost": 0,
        "pvs": null,
        "pvCostAdjustment": 0,
        "ramBytes": 110000000,
        "ramByteRequestAverage": 110000000,
        "ramByteUsageAverage": 48278060.836045,
        "ramByteHours": 586666666.666667,
        "ramCost": 0.001047,
        "ramCostAdjustment": 0,
        "ramEfficiency": 0.438891,
        "sharedCost": 0,
        "externalCost": 0,
        "totalCost": 0.138541,
        "totalEfficiency": 0.0993,
        "rawAllocationOnly": null
      },
      "prometheus": {
        "name": "prometheus",
        "properties": {
          "cluster": "L1-A",
          "namespace": "prometheus"
        },
        "window": {
          "start": "2022-12-16T13:55:23Z",
          "end": "2022-12-19T13:55:23Z"
        },
        "start": "2022-12-19T08:30:00Z",
        "end": "2022-12-19T13:50:00Z",
        "minutes": 320,
        "cpuCores": 0,
        "cpuCoreRequestAverage": 0,
        "cpuCoreUsageAverage": 0.001743,
        "pvCostAdjustment": 0,
        "ramBytes": 0,
        "ramByteRequestAverage": 0,
        "ramByteUsageAverage": 427352097.511181,
        "ramByteHours": 0,
        "ramCost": 0,
        "ramCostAdjustment": 0,
        "ramEfficiency": 0,
        "sharedCost": 0,
        "externalCost": 0,
        "totalCost": 0.004544,
        "totalEfficiency": 0,
        "rawAllocationOnly": null
      }
    }
  ]
}
```