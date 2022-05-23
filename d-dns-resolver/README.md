# Azure private DNS resolver
This demonstrates hybrid DNS solution between Azure and on-prem using Azure Private DNS Resolver on Azure side and Bind on on-prem side.

```bash
az group create -n dns -l westeurope
az bicep build -f infra.bicep
az deployment group create -g dns --template-file infra.json
```

Get IP of DNS resolver that we will point to from onprem.

```bash
az deployment group show -n infra -g dns --query properties.outputs.azureDnsResolverInIp.value -o tsv
```

Get PaaS service URL (used with Private Endpoint from onprem test later)

```bash
az deployment group show -n infra -g dns --query properties.outputs.serviceFqdn.value -o tsv
```

Connect to on-prem DNS server and configure it.

```bash
az serial-console connect -n onpremDnsVm -g dns
sudo -i
apt install -y bind9

cat << EOF > /etc/bind/db.onprem
\$TTL 60
@            IN    SOA  localhost. root.localhost.  (
                          2015112501   ; serial
                          1h           ; refresh
                          30m          ; retry
                          1w           ; expiry
                          30m)         ; minimum
                   IN     NS    localhost.
localhost       A   127.0.0.1
onpremvm.onprem.mydomain.demo.   A       10.99.0.4
EOF

cat << EOF > /etc/bind/named.conf.options
options {
        directory "/var/cache/bind";

        listen-on port 53 { any; };
        allow-query { any; };
        recursion yes;

        auth-nxdomain no;    # conform to RFC1035
};
EOF

cat << EOF > /etc/bind/named.conf.local
// onprem zone
zone "onprem.mydomain.demo" {
  type master;
  file "/etc/bind/db.onprem";
};

// forward to our Azure DNS resolver for cloud domains
zone "azure.mydomain.demo" {
        type forward;
        forwarders {10.1.1.4;};
};
zone "privatelink.blob.core.windows.net" {
        type forward;
        forwarders {10.1.1.4;};
};
EOF

systemctl restart bind9
```

Test from onprem to Azure

```bash
az serial-console connect -n onpremVm -g dns

tomas@onpremVm:~$ dig cloudvm.azure.mydomain.demo

;; ANSWER SECTION:
cloudvm.azure.mydomain.demo. 10 IN      A       10.1.0.4


tomas@onpremVm:~$ dig ydpzynlb3ydfi.blob.core.windows.net

;; ANSWER SECTION:
ydpzynlb3ydfi.blob.core.windows.net. 60 IN CNAME ydpzynlb3ydfi.privatelink.blob.core.windows.net.
ydpzynlb3ydfi.privatelink.blob.core.windows.net. 9 IN A 10.1.0.5
```
Test from Azure to onprem

```bash
az serial-console connect -n cloudVm -g dns

tomas@cloudVm:~$ dig test.onprem.mydomain.demo

;; ANSWER SECTION:
test.onprem.mydomain.demo. 60   IN      A       10.99.0.4
```
