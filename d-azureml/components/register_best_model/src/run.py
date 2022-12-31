import argparse
from pathlib import Path
import pickle
import mlflow
from azureml.core import Run, Experiment

# Get current experiment and root run ID
experiment_name = Run.get_context().parent.experiment.name
root_run_id = Run.get_context().parent.id

print(f"Experiment name: {experiment_name}")
print(f"Root run id: {root_run_id}")

# Find all runs with the same root run ID
filter_string = f"tags.mlflow.rootRunId='{root_run_id}'"
runs = mlflow.search_runs(experiment_names=experiment_name, filter_string=filter_string)

# Print all models
print(runs[["metrics.val_accuracy", "tags.algorithm", "tags.hyperparameters"]].sort_values(by="metrics.val_accuracy", ascending=False))
print("-------------------")

# Find best model
best_model = runs[["run_id", "metrics.val_accuracy", "tags.algorithm", "tags.hyperparameters"]].sort_values(by="metrics.val_accuracy", ascending=False).head(1)
best_run_id = best_model["run_id"].iloc[0]
best_metric = best_model["metrics.val_accuracy"].iloc[0]
best_algorithm = best_model["tags.algorithm"].iloc[0]
best_hyperparameters = best_model["tags.hyperparameters"].iloc[0]

print(f"Best run id: {best_run_id}")
print(f"Best metric: {best_metric}")
print(f"Best algorithm: {best_algorithm}")
print(f"Best hyperparameters: {best_hyperparameters}")

# Register model
model_name = "lending_club"
model_path = f"runs:/{best_run_id}/model"
model = mlflow.register_model(model_uri=model_path, name=model_name)