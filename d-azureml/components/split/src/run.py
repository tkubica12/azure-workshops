import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser("prep")
parser.add_argument("--data", type=str, help="Data file")
parser.add_argument("--label-name", type=str, help="Name of label column")
parser.add_argument("--output-path-train", type=str, help="Path where to save train output files")
parser.add_argument("--output-path-test", type=str, help="Path where to save test output files")
parser.add_argument("--test-size", type=float, help="Percentage of data for test set")
args = parser.parse_args()

print(f"Data file: {args.data}",)
print(f"Label name: {args.label_name}",)
print(f"Output train path: {args.output_path_train}",)
print(f"Output test path: {args.output_path_test}",)

# Load  data
df = pd.read_csv(args.data) 

# Get features and labels
X = df.drop(args.label_name,axis=1).values
y = df[args.label_name].values

# Split data into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

# Save outputs
np.savetxt(args.output_path_train+"/X_train.csv", X_train, delimiter=",")
np.savetxt(args.output_path_test+"/X_test.csv", X_test, delimiter=",")
np.savetxt(args.output_path_train+"/y_train.csv", y_train, delimiter=",")
np.savetxt(args.output_path_test+"/y_test.csv", y_test, delimiter=",")