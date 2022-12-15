import argparse
import pandas as pd
import numpy as np
import mlflow

parser = argparse.ArgumentParser("prep")
parser.add_argument("--x-train", type=str, help="Training features file")
parser.add_argument("--x-test", type=str, help="Testing features file")
parser.add_argument("--y-train", type=str, help="Training labels file")
parser.add_argument("--y-test", type=str, help="Testing labels file")
parser.add_argument("--solver", type=str, help="Solver hyperparameter", default="NoSolverValueReceived")
args = parser.parse_args()

print("args.solver: ", args.solver)

import os
print("AZUREML_SWEEP_solver: ", os.environ.get("AZUREML_SWEEP_solver"))

mlflow.autolog()

# Load data
X_train = np.loadtxt(args.x_train, delimiter=",", dtype=float)
X_test = np.loadtxt(args.x_test, delimiter=",", dtype=float)
y_train = np.loadtxt(args.y_train, delimiter=",", dtype=float)
y_test = np.loadtxt(args.y_test, delimiter=",", dtype=float)

# Fit model
from sklearn.linear_model import LogisticRegression

classifier = LogisticRegression(random_state = 42, max_iter=1000, solver=args.solver)
classifier.fit(X_train, y_train)

# Make predictions
y_pred = classifier.predict(X_test)

# Log metrics
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

mlflow.log_metric("val_accuracy", accuracy_score(y_test, y_pred))
mlflow.log_metric('val_precision',precision_score(y_test, y_pred))
mlflow.log_metric('val_recall',recall_score(y_test, y_pred))
mlflow.log_metric('val_f1',f1_score(y_test, y_pred))
