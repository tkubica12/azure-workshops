import argparse
import pandas as pd
import numpy as np
import mlflow

parser = argparse.ArgumentParser("prep")
parser.add_argument("--x-train", type=str, help="Training features file")
parser.add_argument("--x-test", type=str, help="Testing features file")
parser.add_argument("--y-train", type=str, help="Training labels file")
parser.add_argument("--y-test", type=str, help="Testing labels file")
parser.add_argument("--model", type=str, help="Filename for resulting model to be saved")
args = parser.parse_args()

mlflow.autolog()

# Load data
X_train = np.loadtxt(args.x_train, delimiter=",", dtype=float)
X_test = np.loadtxt(args.x_test, delimiter=",", dtype=float)
y_train = np.loadtxt(args.y_train, delimiter=",", dtype=float)
y_test = np.loadtxt(args.y_test, delimiter=",", dtype=float)

# Fit model
from sklearn.linear_model import LogisticRegression

classifier = LogisticRegression(random_state = 42, max_iter=1000)
classifier.fit(X_train, y_train)

# Make predictions
y_pred = classifier.predict(X_test)

