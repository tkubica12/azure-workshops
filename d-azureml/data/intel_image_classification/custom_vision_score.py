from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import os
import argparse
import urllib
from zipfile import ZipFile

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--prediction-endpoint", help="Prediction endpoint for Custom Vision", required=True)
parser.add_argument("--prediction-key", help="Prediction key for Custom Vision", required=True)
parser.add_argument("--project-id", help="Custom Vision project id", required=True)
parser.add_argument("--publish-name", help="Published iteration name", required=True)
parser.add_argument("--data_path", type=str, default="./localdata", help="Dataset location")
args = parser.parse_args()

print(f"Using prediction endpoint {args.prediction_endpoint}, prediction key {args.prediction_key}, data path {args.data_path}")

# Download test data
dir = args.data_path
url = "https://tkubicastore.blob.core.windows.net/datasets/IntelImageClassification-test.zip?sp=r&st=2023-01-10T07:35:28Z&se=2050-01-10T15:35:28Z&spr=https&sv=2021-06-08&sr=b&sig=ll4OfueLALA4O0kMMNeOr5A10aQMWXOruUO%2F5cryocE%3D"
os.makedirs(dir, exist_ok=True)
print(f"Downloading data from {url}")
dataset_name = "custom_vision_intel_image_classification_test"
dataset_dir = os.path.join(dir, dataset_name)

urllib.request.urlretrieve(url, filename="data.zip")

with ZipFile("data.zip", "r") as zip:
    print("Extracting files")
    zip.extractall(path=dataset_dir)
    print("Extraction complete")
os.remove("data.zip")


# Custom Vision prediction client
print("Getting client")
credentials = ApiKeyCredentials(in_headers={"Prediction-key": args.prediction_key})
predictor = CustomVisionPredictionClient(args.prediction_endpoint, credentials)


# Score images - each class in a separate folder
correct = 0
total = 0

dataset_base_dir = os.path.join(dataset_dir, os.listdir(dataset_dir)[0])
for class_name in os.listdir(dataset_base_dir):
    sub_dir = os.path.join(dataset_base_dir, class_name)
    if not os.path.isdir(sub_dir):
        continue

    print(f"\n\nProcessing {sub_dir}")
    for image in os.listdir(sub_dir):
        results = predictor.classify_image(args.project_id, args.publish_name, open(os.path.join(sub_dir, image), "rb").read())
        if results.predictions[0].tag_name == class_name:
            correct += 1
            total += 1
        else:
            total += 1
        print(f"Correct {correct} out of {total} ({correct/total*100:.2f}%)")