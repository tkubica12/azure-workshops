import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


parser = argparse.ArgumentParser("prep")
parser.add_argument("--output-path-train", type=str, help="Path where to save train output files")
parser.add_argument("--input-x-train", type=str, help="File where to expect train input files")
parser.add_argument("--input-y-train", type=str, help="File where to expect train input files")
args = parser.parse_args()

print(f"Output train path: {args.output_path_train}",)
print(f"Input x train file: {args.input_x_train}",)
print(f"Input y train file: {args.input_y_train}",)

# Load  data
X_train = np.loadtxt(args.input_x_train, delimiter=",", dtype=float)
y_train = np.loadtxt(args.input_y_train, delimiter=",", dtype=float)

# Oversample train data to get more balanced label
from imblearn.over_sampling import SMOTE
sm = SMOTE(random_state = 2)
X_train, y_train = sm.fit_resample(X_train, y_train.ravel())

# Save outputs
np.savetxt(args.output_path_train+"/X_train.csv", X_train, delimiter=",")
np.savetxt(args.output_path_train+"/y_train.csv", y_train, delimiter=",")