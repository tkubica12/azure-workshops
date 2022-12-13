# Azure ML demo

## Deploy infrastructure

```bash
cd terraform
terraform init
terraform apply -auto-approve

export rg=$(terraform output -raw resource_group_name)
export aml=$(terraform output -raw azureml_workspace_name)
export aksid=$(terraform output -raw aksid)
export amlidentity=$(terraform output -raw amlidentity)
```

## Install or update Azure ML CLI

```bash
az extension add --upgrade -n ml
```

## Attach AKS to Azure ML workspace

```bash
az ml compute attach --name ml-aks \
    -g d-azurelm \
    --workspace-name $aml \
    --type Kubernetes  \
    --resource-id $aksid \
    --identity-type UserAssigned  \
    --namespace azureml \
    --user-assigned-identities $amlidentity
```

## Deploy Azure ML stuff

```bash
cd ..

# Register data
az ml data create -f data/lending_club_raw.yaml -g $rg -w $aml

# Create components
az ml component create -f components/lending_club_process_data/component.yaml -g $rg -w $aml
az ml component create -f components/split_and_scale/component.yaml -g $rg -w $aml
az ml component create -f components/lending_club_train_tensorflow/component.yaml -g $rg -w $aml
az ml component create -f components/lending_club_train_lr/component.yaml -g $rg -w $aml
az ml component create -f components/reference_model_always_one/component.yaml -g $rg -w $aml
#az ml component create -f components/register_model/component.yaml -g $rg -w $aml

# Create pipeline
az ml job create -f pipelines/lending_club_pipeline.yaml -g $rg -w $aml
```

# Destroy infrastructure

```bash
cd terraform
terraform destroy -auto-approve
```
