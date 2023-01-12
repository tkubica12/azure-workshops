# Azure ML demo

This demo contains ML pipelines:
- CLI v2 is used so steps can be easily automated in CI/CD pipeline
- Reusable components are used to split, scale and oversample data (currently demo does not use oversampling as data are not badly imbalanced and prediction get worse when used - nevertheless for demo purposes it is part of pipeline and used for reference model)
- Currently 3 models are implemented and some with hyperparameter tuning:
  - Reference model that always answer "one" on binary classification to set baseline for metrics such as accuracy
  - Classic sklearn Logistic Regression with hyperparameter tuning over solver
  - Tensorflow deep learning model 150-75-37-18-1 with various dropout rates tried via hyperparameter tuning
- After all runs best model is selected and registered in Azure ML
- Managed compute is used by default for training
- Template includes bring your own AKS cluster scenario - enabled it on input eg. by modifying default.auto.tfvars
- Custom environment (Docker image) is used for oversampling component (to include imbalanced-learn library)

Another demo focuses on image classification in computer vision category:
- Pipeline with custom simple CNN model
- Pipeline with custom ResNet50 transfer learning model
- AutoML pipeline
- Azure Cognitive Services Custom Vision to compare AML with cognitive services

## Deploy infrastructure
This step is required for all demos. Look into default.auto.tfvars file in terraform to set input parameters. By default we are deploying managed clusters, but you can also deploy separate AKS cluster that you can attach to Azure ML.

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
For CLI commands make sure you have latest version of Azure CLI extension.

```bash
az extension add --upgrade -n ml
```

## Attach AKS to Azure ML workspace
Optionally if you have deployed AKS cluster Terraform built it together with proper extensions so it is ready to be attached to Azure ML workspace. If you use managed compute you can skip this step.

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

## Lending club demo
First demo is focused on showcasing complex pipeline with multiple models and hyperparameter tuning and MLOps. It is based on Lending Club dataset and binary classification problem - predicting what lenders will default (do not pay) on their loans.

You will now register data, environments, components and finally deploy pipeline.

```bash
cd ..

# Register data
az ml data create -f data/lending_club_raw.yaml -g $rg -w $aml
az ml data create -f data/lending_club_inferencing.yaml -g $rg -w $aml
az ml data create -f data/lending_club_mltable.yaml -g $rg -w $aml

# Create environments
az ml environment create -f environments/imblearn/environment.yaml -g $rg -w $aml

# Create components
az ml component create -f components/split/component.yaml -g $rg -w $aml
az ml component create -f components/scale/component.yaml -g $rg -w $aml
az ml component create -f components/oversample/component.yaml -g $rg -w $aml
az ml component create -f components/reference_model_always_one/component.yaml -g $rg -w $aml
az ml component create -f components/register_best_model/component.yaml -g $rg -w $aml

# Create training pipeline
az ml job create -f pipelines/lending_club_training.yaml -g $rg -w $aml
```

Here is resulting pipeline visualization.

![Pipeline](./images/pipeline.png)

## Intel Image Classification demo
This demo showcases image classification problem using Azure ML and Azure Cognitive Services Custom Vision. It is based on Intel Image Classification dataset. 

Scenarios in Azure ML:
- Custom CNN model
- Custom transfer learning model using variant of resnet trained on ImageNet
- AutoML

For comparison there is also solution in high-level Custom Vision service.


### Azure ML

```bash
# Download data source, upload to Azure ML and create metadata (annotations and MLTable files)
cd data/intel_image_classification
python prep.py --subscription d3b7888f-c26e-4961-a976-ff9d5b31dfd3 --group d-azurelm --workspace aml-am0bg611
cd ../..

# Create MLTables
# az ml data create -f data/intel_image_classification/train.yaml -g $rg -w $aml
# az ml data create -f data/intel_image_classification/test.yaml -g $rg -w $aml

# Create training pipeline
az ml job create -f pipelines/intel_image_class_automl_small.yaml -g $rg -w $aml
az ml job create -f pipelines/intel_image_class_automl_large.yaml -g $rg -w $aml
az ml job create -f pipelines/intel_image_class_cnn.yaml -g $rg -w $aml
az ml job create -f pipelines/intel_image_class_resnet.yaml -g $rg -w $aml
```

### Custom Vision

```bash
# Install SDK
pip install azure-cognitiveservices-vision-customvision

# From UI get endpoint and key and upload data using script
cd data/intel_image_classification
python custom_vision_upload.py --training-endpoint https://northeurope.api.cognitive.microsoft.com/ --training-key a5e94be5af04427296bd604f3d8f505d
```

In UI run training with 6 hours budget. Then publish model and get its endpoint and key.

Score model using script:

```bash
python custom_vision_score.py --prediction-endpoint https://northeurope.api.cognitive.microsoft.com/ --prediction-key 2d4c9330d93a4c4c87a58f1b38fc22c5 --project-id 90818496-fef6-4183-ba51-18dfdaefba77 --publish-name mymodel
```

# Destroy infrastructure
After all experiments yoy can destroy infrastructure.

```bash
cd terraform
terraform destroy -auto-approve
```

# Additional notes
local_dev folder contains notebooks that I used to develop and test code for components in pipeline before using it in Azure ML.

