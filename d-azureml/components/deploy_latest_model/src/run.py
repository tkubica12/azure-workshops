import argparse
from pathlib import Path
import pickle
import mlflow

parser = argparse.ArgumentParser("prep")
parser.add_argument("--model-name", type=str, help="Name of model to deploy")
args = parser.parse_args()

# Get latest version of registered model
client = mlflow.MlflowClient()

model_name = args.model_name
model_version = client.get_registered_model(model_name).latest_versions[0].version

print(f"Latest version of model {model_name} is {model_version}")

# Create deployment configuration
import json

deploy_config = {
   "instance_type": "Standard_DS2_v2",
   "instance_count": 1,
}

deployment_config_path = "deployment_config.json"
with open(deployment_config_path, "w") as outfile:
   outfile.write(json.dumps(deploy_config))

# Deploy model
from mlflow.deployments import get_deploy_client

deploy_client = get_deploy_client(client.tracking_uri)

deploy_client.create_deployment(
   model_uri=f"models:/{model_name}/{model_version}",
   config={ "deploy-config-file": deployment_config_path },
   name=f"landing-club-{model_version}",
)

