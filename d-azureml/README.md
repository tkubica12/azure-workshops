# Azure ML demo

## Deploy infrastructure

```bash
cd terraform
terraform init
terraform apply -auto-approve

export rg=$(terraform output -raw resource_group_name)
export aml=$(terraform output -raw azureml_workspace_name)
```

## Deploy Azure ML stuff

```bash
# Register data
az ml data create -f data/lending_club.yaml -g $rg -w $aml

# Create component
az ml component create -f components/download_repo.yaml -g $rg -w $aml

# Create pipeline
az ml job create -f pipelines/lending_club_pipeline.yaml -g $rg -w $aml


```