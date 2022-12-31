import argparse
import pandas as pd
import numpy as np
import mlflow


parser = argparse.ArgumentParser("prep")
parser.add_argument("--x-train", type=str, help="Training features file")
parser.add_argument("--x-test", type=str, help="Testing features file")
parser.add_argument("--y-train", type=str, help="Training labels file")
parser.add_argument("--y-test", type=str, help="Testing labels file")
parser.add_argument("--saved-scaler", type=str, help="SSaved scaler file to log with model as artefact")
parser.add_argument("--num-leaves", type=int, help="Number of leaves hyperparameter")
parser.add_argument("--finished", type=str)
args = parser.parse_args()

# Load data
X_train = np.loadtxt(args.x_train, delimiter=",", dtype=float)
X_test = np.loadtxt(args.x_test, delimiter=",", dtype=float)
y_train = np.loadtxt(args.y_train, delimiter=",", dtype=float)
y_test = np.loadtxt(args.y_test, delimiter=",", dtype=float)

# Set tag
mlflow.set_tag("algorithm", "LightGBM")

# Log scaler artefact
mlflow.log_artifact(args.saved_scaler, "model")

# Fit model
from lightgbm import LGBMClassifier

classifier = LGBMClassifier(num_leaves=args.num_leaves)
classifier.fit(X_train, y_train)

# Log model
mlflow.lightgbm.log_model(classifier, "model")

# Log parameters
mlflow.log_param("num_leaves", classifier.num_leaves)

# Make predictions
y_pred = classifier.predict(X_test)

# Log metrics
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, auc

mlflow.log_metric("val_accuracy", accuracy_score(y_test, y_pred))
mlflow.log_metric('val_precision',precision_score(y_test, y_pred))
mlflow.log_metric('val_recall',recall_score(y_test, y_pred))
mlflow.log_metric('val_f1',f1_score(y_test, y_pred))

print(f"val_accuracy: {accuracy_score(y_test, y_pred)}")

# Finished
from pathlib import Path
Path(args.finished).touch()