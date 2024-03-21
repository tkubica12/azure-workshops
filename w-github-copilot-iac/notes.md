1. chat only

I have following data structure

storages:
  - name: tomaskubicastorage01
    replication: LRS
    private_endpoint_enabled: true
  - name: tomaskubicastorage02
    replication: ZRS
    private_endpoint_enabled: false

Convert it to local in Terraform

2. ask for RG and provider
3. Ask to create storage. If mapping, ask for what it is and replace locals with it and refactor. If using count, ask whether it is a good practice.
4. Refactor with maps
5. Ask to add private endpoint
6. Explain what for_each does on my own data
7. Replace locals with vars - default value, schema, rich description
8. Paste error and ask to fix it