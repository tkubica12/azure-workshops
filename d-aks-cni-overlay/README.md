# AKS with Azure CNI overlay mode to replace Kubenet


Register feature

```bash
az feature register --namespace Microsoft.ContainerService --name AzureOverlayPreview
```

Deploy Kubernetes apps

```bash
az aks get-credentials -n d-aks-cni-overlay -g d-aks-cni-overlay-aks --admin --overwrite
kubectl apply -f ./kubernetes
```

Get httpbin ACI IP

```bash
az container show -n httpbin -g d-aks-cni-overlay-aks --query ipAddress.ip -o tsv
```

Jump to container in Kubernetes and check outbound IP by calling httpbin.

```bash
kubectl exec -ti client -- /bin/bash

: `
curl 10.99.3.4/ip 
{
  "origin": "10.99.2.4"
}
`
```

Get IP addresses of Pods, connect to one of Pods and initiate curl to other one.

```bash
kubectl get pods
kubectl exec -ti mypod123 -- /bin/bash -c "curl 10.1.2.3"
```

In different window we will open privileged container running on host network so we can sniff packets comming to Node. We can filter tcpdump based on IP of one of our Pods and discover that there is direct communication between Pods - no VXLAN or different type of tunnel

```bash
tcpdump -env host 10.244.2.254

: 'tcpdump: listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
17:55:59.070885 cc:46:d6:24:69:2f > 60:45:bd:22:ff:b8, ethertype IPv4 (0x0800), length 74: (tos 0x0, ttl 63, id 5921, offset 0, flags [DF], proto TCP (6), length 60)
    10.244.1.129.49136 > 10.244.2.254.80: Flags [S], cksum 0x872f (correct), seq 1278312572, win 64240, options [mss 1410,sackOK,TS val 931718964 ecr 0,nop,wscale 7], length 0
17:55:59.071155 60:45:bd:22:ff:b8 > 12:34:56:78:9a:bc, ethertype IPv4 (0x0800), length 74: (tos 0x0, ttl 63, id 0, offset 0, flags [DF], proto TCP (6), length 60)     
    10.244.2.254.80 > 10.244.1.129.49136: Flags [S.], cksum 0x1a95 (incorrect -> 0xf527), seq 3702892630, ack 1278312573, win 65160, options [mss 1460,sackOK,TS val 1434629021 ecr 931718964,nop,wscale 7], length 0
17:55:59.072248 cc:46:d6:24:69:2f > 60:45:bd:22:ff:b8, ethertype IPv4 (0x0800), length 66: (tos 0x0, ttl 63, id 5922, offset 0, flags [DF], proto TCP (6), length 52)  
    10.244.1.129.49136 > 10.244.2.254.80: Flags [.], cksum 0x2086 (correct), ack 1, win 502, options [nop,nop,TS val 931718965 ecr 1434629021], length 0
17:55:59.072248 cc:46:d6:24:69:2f > 60:45:bd:22:ff:b8, ethertype IPv4 (0x0800), length 142: (tos 0x0, ttl 63, id 5923, offset 0, flags [DF], proto TCP (6), length 128)
    10.244.1.129.49136 > 10.244.2.254.80: Flags [P.], cksum 0xe5f8 (correct), seq 1:77, ack 1, win 502, options [nop,nop,TS val 931718966 ecr 1434629021], length 76: HTTP, length: 76
        GET / HTTP/1.1
        Host: 10.244.2.254
        User-Agent: curl/7.74.0
        Accept: */*

17:55:59.072305 60:45:bd:22:ff:b8 > 12:34:56:78:9a:bc, ethertype IPv4 (0x0800), length 66: (tos 0x0, ttl 63, id 24940, offset 0, flags [DF], proto TCP (6), length 52) 
    10.244.2.254.80 > 10.244.1.129.49136: Flags [.], cksum 0x1a8d (incorrect -> 0x2031), ack 77, win 509, options [nop,nop,TS val 1434629022 ecr 931718966], length 0  
17:55:59.072441 60:45:bd:22:ff:b8 > 12:34:56:78:9a:bc, ethertype IPv4 (0x0800), length 304: (tos 0x0, ttl 63, id 24941, offset 0, flags [DF], proto TCP (6), length 290)
    10.244.2.254.80 > 10.244.1.129.49136: Flags [P.], cksum 0x1b7b (incorrect -> 0x776c), seq 1:239, ack 77, win 509, options [nop,nop,TS val 1434629023 ecr 931718966], length 238: HTTP, length: 238
        HTTP/1.1 200 OK
        Server: nginx/1.23.1
'
```

