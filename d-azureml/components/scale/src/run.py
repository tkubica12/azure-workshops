import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


parser = argparse.ArgumentParser("prep")
parser.add_argument("--output-path-train", type=str, help="Path where to save train output files")
parser.add_argument("--output-path-test", type=str, help="Path where to save test output files")
parser.add_argument("--output-file-scaler", type=str, help="File to save scaler")
parser.add_argument("--input-x-train", type=str, help="File where to expect train input files")
parser.add_argument("--input-y-train", type=str, help="File where to expect train input files")
parser.add_argument("--input-x-test", type=str, help="File where to expect test input files")
parser.add_argument("--input-y-test", type=str, help="File where to expect test input files")
args = parser.parse_args()

print(f"Output train path: {args.output_path_train}",)
print(f"Output test path: {args.output_path_test}",)
print(f"Output scaler file: {args.output_file_scaler}",)
print(f"Input x train file: {args.input_x_train}",)
print(f"Input y train file: {args.input_y_train}",)
print(f"Input x test file: {args.input_x_test}",)
print(f"Input y test file: {args.input_y_test}",)

# Load  data
X_train = np.loadtxt(args.input_x_train, delimiter=",", dtype=float)
X_test = np.loadtxt(args.input_x_test, delimiter=",", dtype=float)
y_train = np.loadtxt(args.input_y_train, delimiter=",", dtype=float)
y_test = np.loadtxt(args.input_y_test, delimiter=",", dtype=float)

# Scale features
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save scaler
import joblib
joblib.dump(scaler, args.output_file_scaler)

# Save outputs
np.savetxt(args.output_path_train+"/X_train.csv", X_train, delimiter=",")
np.savetxt(args.output_path_test+"/X_test.csv", X_test, delimiter=",")
np.savetxt(args.output_path_train+"/y_train.csv", y_train, delimiter=",")
np.savetxt(args.output_path_test+"/y_test.csv", y_test, delimiter=",")