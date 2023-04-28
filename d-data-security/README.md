# Data security
This repo contains examples of data security in Azure including:
- Using customer managed keys to encrypt data at rest and data in use including Azure Disks, Azure Storage and Azure SQL Database.
- Storing data in immutable way using Blobs immutability, Azure Confidential Ledger or Azure SQL Ledger.
- Encrypting data in use with Confidential Computing using Confidential VMs and Azure SQL Database Alwayes Encrypted with Confidential Computing.
- Confidential Computing with Azure Kubernetes Service - SGX containers, Kata containers, Confidential nodes, Kata Confidential Containers
  
To deploy use terraform folder and modify demo.auto.tfvars to enable features/demos you are interested in.

## Azure Disk encryption (ADE)
Demonstrate OS-level encryption with Bitlocker integration on vm-ade and Customer Managed Key (CMK) in Portal or in VM.

## Azure Disk server-side encryption (SSE)
Demonstrate use of double-key encryption with Platform Managed Key (PMK) + Customer Managed Key (CMK) in Portal.

## Azure Confidential VM
Some of the VMs are configured as confidential VMs.

## Confidential computing on AKS
AKS cluster currently includes:
- default nodepool with standard VM
- SGX-enabled nodepool for enclave-aware containers
- Kata containers enabled nodepool for nested-virtualization isolation of unmodified containers
- Confidential nodes using SEV-SNP
- (FUTURE) Kata Confidential Containers for nested-virtualization isolation of unmodified containers with SEV-SNP

| Solution | Protect against cloud provider | Protect against node administrator | Protect against privileged containers | Full isolation between containers | Works with existing apps | Works with all Kubernetes addons |
| --- | --- | --- | --- | --- | --- | --- |
| Standard nodes | No | No | No | No | Yes | Yes |
| SXG enclave-aware | Yes | Yes | Yes | No | No | Yes |
| Kata containers | No | No | Yes | Yes | Yes | No |
| Confidential nodes | Yes | No | No | No | Yes | Yes |
| (FUTURE) Kata Confidential Containers | Yes | Yes | Yes | Yes | Yes | No |


### SGX-enabled nodepool
Go to SGX VMSS, node and use Bastion to connect to node.

Install procmon and dump standard process - both variables can be seen plain text in dump.

```bash
sudo apt install procdump
sudo ps aux | grep app
sudo procdump 17213 standard.dmp
sudo grep mypassword standard.dmp.17213   # MATCH
sudo grep mysecurepassword standard.dmp.17213   # MATCH
```

Repeat for SGX protected application where secure part runs in enclave so it is not plain text visible in dump.

```bash
sudo apt install procdump
sudo ps aux | grep start_host
sudo procdump 17787 sgx.dmp
sudo grep mypassword sgx.dmp.17787 # MATCH
sudo grep mysecurepassword sgx.dmp.17787 #  MISS
```

Things to note:
- Trusted execution even you do not trust cloud provider, node admin or privileged containers
- Requires specifically written application (eg. using Open Enclave SDK, SGX SDK, EGo, Confidential Inferencing ONNX Runtime) or some framework to handle existing stuff (Fortanix, SCONE, Anjuna, Gramine, Occlum, Marblerun)
- Standard highly efficient solution (normal Kubernetes, no virtualization overhead, standard monitoring, ...)

### Kata nodes (nested virtualization)
Go to Kata VMSS, node and use Bastion to connect to node.

Check this time process is not visible in kernel, because container runs in nested virtualization with its own kernel.

```bash
sudo ps aux | grep app  # /app process not here
sudo ps aux | grep cloud-hypervisor # see api socket for VM
sudo ch-remote --api-socket /run/vc/vm/18014e2695fe49d3461e63ff753cd6c392430a6f3bdfe76525844bd433dc8db1/clh-api.sock info # This is our VM
```

Let's not use avml tool to dump whole node memory. We can see plain text variables in dump.

```bash
wget https://github.com/microsoft/avml/releases/download/v0.11.2/avml
chmod +x ./avml
sudo ./avml dump

sudo grep mypassword dump # MATCH
sudo grep mysecurepassword dump # MATCH
```

Things to note:
- Kata containers are giving stronger isolation between containers, but do not protect against untrusted cloud provider or node administrator
- Less efficient from perspective of resource sharing or speed of startup
- Not standard container therefore some features and addons might not work out of the box (some monitoring and security tools as an example, eBPF-based tools, service meshes, some CSI providers)

### Confidential nodes using SEV-SNP
Go to sevsnp VMSS, node and use Bastion to connect to node.

Install procmon and dump standard process - both variables can be seen plain text in dump.

```bash
sudo apt install procdump
sudo ps aux | grep app
sudo procdump 17213 standard.dmp
sudo grep mypassword standard.dmp.17213   # MATCH
sudo grep mysecurepassword standard.dmp.17213   # MATCH
```

Things to note:
- Confidential nodes encrypt memory and protect against untrusted cloud provider, but do not protect against node administrator or privileged containers

## Azure SQL Database data-at-rest encryption
Demonstrate Transparent Data Encryption (TDE) with Customer Managed Key (CMK) in Portal.

## Azure SQL Ledger
Connect to database 

```sql
-- Create updatable table
CREATE TABLE dbo.MyAuditedTable (
    Message nvarchar(100)
)
WITH (SYSTEM_VERSIONING = ON, LEDGER = ON);
GO

-- Insert and than update some data
INSERT INTO dbo.MyAuditedTable (Message) VALUES ('My first message'), ('My second message'), ('My third message');

UPDATE dbo.MyAuditedTable 
SET Message = 'My modified message' 
WHERE Message = 'My first message';

-- See table history
SELECT TOP (1000) * FROM [dbo].[MyAuditedTable] ORDER BY ledger_transaction_id

-- See hashes of operations -> this is what gets stored in immutable storage or Azure Confidential Ledger
SELECT * FROM sys.database_ledger_transactions

-- You can add new data
INSERT INTO dbo.MyAuditedTable (Message) VALUES ('My another message');
```

## Azure SQL Always Encrypted with Confidential Computing
In portal note Attestation service URL and configure policy of type SGX-IntelSDK by selecting Test format and pasting this:


```
version= 1.0;
authorizationrules 
{
       [ type=="x-ms-sgx-is-debuggable", value==false ]
        && [ type=="x-ms-sgx-product-id", value==4639 ]
        && [ type=="x-ms-sgx-svn", value>= 0 ]
        && [ type=="x-ms-sgx-mrsigner", value=="e31c9e505f37a58de09335075fc8591254313eb20bb1a27e5443cc450b6e33e5"] 
    => permit();
};
```

Create table and fill it with data

```sql
-- Create tables
CREATE TABLE dbo.MySecretData (
    MyData nvarchar(100)
)
GO

CREATE TABLE dbo.MyUnprotectedData (
    MyData nvarchar(100)
)
GO

-- Insert data
INSERT INTO dbo.MySecretData (MyData) VALUES ('secret1'), ('secret2'), ('secret3');
INSERT INTO dbo.MyUnprotectedData (MyData) VALUES ('secret1'), ('secret2'), ('secret3');
```

Connect to DB with SQL Server Management Studio with Always Encrypted enabled and follow guides here [https://learn.microsoft.com/en-us/azure/azure-sql/database/always-encrypted-enclaves-getting-started](https://learn.microsoft.com/en-us/azure/azure-sql/database/always-encrypted-enclaves-getting-started)