# Data security
This repo contains examples of data security in Azure including:
- Using customer managed keys to encrypt data at rest and data in use including Azure Disks, Azure Storage and Azure SQL Database.
- Storing data in immutable way using Blobs immutability, Azure Confidential Ledger or Azure SQL Ledger.
- Encrypting data in use with Confidential Computing using Confidential VMs and Azure SQL Database Alwayes Encrypted with Confidential Computing.
  
## Azure Disk encryption (ADE)
Demonstrate OS-level encryption with Bitlocker integration on vm-ade and Customer Managed Key (CMK) in Portal or in VM.

## Azure Disk server-side encryption (SSE)
Demonstrate use of double-key encryption with Platform Managed Key (PMK) + Customer Managed Key (CMK) in Portal.

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