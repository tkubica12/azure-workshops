# Data security
This repo contains examples of data security in Azure including:
- Using customer managed keys to encrypt data at rest and data in use including Azure Disks, Azure Storage and Azure SQL Database.
- Storing data in immutable way using Blobs immutability, Azure Confidential Ledger or Azure SQL Ledger.
- Encrypting data in use with Confidential Computing using Confidential VMs and Azure SQL Database Alwayes Encrypted with Confidential Computing.
  
## Azure Disk encryption (ADE)
Demonstrate OS-level encryption with Bitlocker integration on vm-ade and Customer Managed Key (CMK).

## Azure Disk server-side encryption (SSE)
Using double-key encryption with Platform Managed Key (PMK) + Customer Managed Key (CMK).

## Azure SQL Database data-at-rest encryption
This demo uses Transparent Data Encryption (TDE) with Customer Managed Key (CMK).