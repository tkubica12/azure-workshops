import argparse
import pandas as pd
import numpy as np
import mlflow

parser = argparse.ArgumentParser("prep")
parser.add_argument("--x-train", type=str, help="Training features file")
parser.add_argument("--x-test", type=str, help="Testing features file")
parser.add_argument("--y-train", type=str, help="Training labels file")
parser.add_argument("--y-test", type=str, help="Testing labels file")
args = parser.parse_args()

mlflow.autolog()

# Load data
X_train = np.loadtxt(args.x_train, delimiter=",", dtype=float)
X_test = np.loadtxt(args.x_test, delimiter=",", dtype=float)
y_train = np.loadtxt(args.y_train, delimiter=",", dtype=float)
y_test = np.loadtxt(args.y_test, delimiter=",", dtype=float)

# Evaluate model
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

# Make predictions
y_pred = np.ones(y_test.shape, dtype=np.int32)

# Evaluate model
print ("Confusion Matrix : \n", confusion_matrix(y_test, y_pred))
print ("Accuracy : ", accuracy_score(y_test, y_pred))
print ("Precision : ", precision_score(y_test, y_pred))
print ("Recall : ", recall_score(y_test, y_pred))
print ("F1 Score : ", f1_score(y_test, y_pred))

# Log metrics with MLflow
mlflow.log_metric('val_accuracy',accuracy_score(y_test, y_pred))
mlflow.log_metric('val_precision',precision_score(y_test, y_pred))
mlflow.log_metric('val_recall',recall_score(y_test, y_pred))
mlflow.log_metric('val_f1',f1_score(y_test, y_pred))