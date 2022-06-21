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
az ml data create -f data/lending_club_raw.yaml -g $rg -w $aml

# Create components
az ml component create -f components/lending_club_process_data/component.yaml -g $rg -w $aml
az ml component create -f components/split_and_scale/component.yaml -g $rg -w $aml
az ml component create -f components/lending_club_train/component.yaml -g $rg -w $aml

# Create pipeline
az ml job create -f pipelines/lending_club_pipeline.yaml -g $rg -w $aml
```

# Destroy infrastructure

```bash
cd terraform
terraform destroy -auto-approve
```