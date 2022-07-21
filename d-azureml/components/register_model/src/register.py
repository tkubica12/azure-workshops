import argparse
from pathlib import Path
import pickle

import mlflow

from azureml.core import Run

# Get run
run = Run.get_context()
run_id = run.get_details()["runId"]
print(run_id)

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name', type=str, help='Name under which model will be registered')
    parser.add_argument('--model-path', type=str, help='Model directory')
    
    args, _ = parser.parse_known_args()
    print(f'Arguments: {args}')

    return args


def main():

    args = parse_args()

    model_name = args.model_name
    model_path = args.model_path

    print("Registering ", model_name)

    model = pickle.load(open((Path(model_path) / "model.pkl"), "rb"))

    # log model using mlflow 
    mlflow.sklearn.log_model(model, model_name)

    # register model using mlflow model
    model_uri = f'runs:/{run_id}/{args.model_name}'
    mlflow.register_model(model_uri, model_name)
        
if __name__ == "__main__":
    main()