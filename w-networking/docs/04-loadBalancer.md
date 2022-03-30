## 04 - Using standard L4 Azure Load Balancers
Let's deploy web application to our servers and use Azure LB to load balance traffic.

First let's install web application on our front VMs.

```bash
# Configure prefix (in bash)
export prefix=tomaskubica4

# Configure prefix (in PowerShell)
$prefix="tomaskubica4"

# Install front1
az serial-console connect -n $prefix-front1 -g $prefix-project1
sudo apt update && sudo apt install -y nginx
echo "My WEB on node 1" | sudo tee /var/www/html/index.html

# Install front2
az serial-console connect -n $prefix-front2 -g $prefix-project1
sudo apt update && sudo apt install -y nginx
echo "My WEB on node 2" | sudo tee /var/www/html/index.html
```

We will now configure Load Balancer.

```bash
# BASH

# Create LB
az network lb create -n $prefix-lb \
    -g $prefix-project1 \
    --sku Standard \
    --vnet-name $prefix-project1 \
    --subnet frontend \
    --frontend-ip-name $prefix-lb-frontend \
    --backend-pool-name $prefix-lb-backend \
    --private-ip-address 10.1.1.100

# Create health probe
az network lb probe create -n myprobe \
    -g $prefix-project1 \
    --lb-name $prefix-lb \
    --protocol tcp \
    --port 80

# Create rule
az network lb rule create -n webrule \
    -g $prefix-project1 \
    --lb-name $prefix-lb \
    --protocol tcp \
    --frontend-port 80 \
    --backend-port 80 \
    --frontend-ip-name $prefix-lb-frontend \
    --backend-pool-name $prefix-lb-backend \
    --probe-name myprobe \
    --idle-timeout 15 \
    --enable-tcp-reset true

# Add both NIC configs to backend pool
az network nic ip-config address-pool add \
    -g $prefix-project1 \
   --address-pool $prefix-lb-backend \
   --ip-config-name ipconfig${prefix}-front1 \
   --nic-name $prefix-front1VMNic \
   --lb-name $prefix-lb

az network nic ip-config address-pool add \
    -g $prefix-project1 \
   --address-pool $prefix-lb-backend \
   --ip-config-name ipconfig${prefix}-front2 \
   --nic-name $prefix-front2VMNic \
   --lb-name $prefix-lb
```

```powershell
# PowerShell

# Create LB
az network lb create -n $prefix-lb `
    -g $prefix-project1 `
    --sku Standard `
    --vnet-name $prefix-project1 `
    --subnet frontend `
    --frontend-ip-name $prefix-lb-frontend `
    --backend-pool-name $prefix-lb-backend `
    --private-ip-address 10.1.1.100

# Create health probe
az network lb probe create -n myprobe `
    -g $prefix-project1 `
    --lb-name $prefix-lb `
    --protocol tcp `
    --port 80

# Create rule
az network lb rule create -n webrule `
    -g $prefix-project1 `
    --lb-name $prefix-lb `
    --protocol tcp `
    --frontend-port 80 `
    --backend-port 80 `
    --frontend-ip-name $prefix-lb-frontend `
    --backend-pool-name $prefix-lb-backend `
    --probe-name myprobe `
    --idle-timeout 15 `
    --enable-tcp-reset true

# Add both NIC configs to backend pool
az network nic ip-config address-pool add `
    -g $prefix-project1 `
   --address-pool $prefix-lb-backend `
   --ip-config-name ipconfig${prefix}-front1 `
   --nic-name $prefix-front1VMNic `
   --lb-name $prefix-lb

az network nic ip-config address-pool add `
    -g $prefix-project1 `
   --address-pool $prefix-lb-backend `
   --ip-config-name ipconfig${prefix}-front2 `
   --nic-name $prefix-front2VMNic `
   --lb-name $prefix-lb
```


Test balancing.

```bash
az serial-console connect -n $prefix-jump -g $prefix-project1
while true; do curl 10.1.1.100 --local-port $[$RANDOM+20000]; sleep 0.1; done
```