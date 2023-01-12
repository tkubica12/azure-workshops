from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
# from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid
import argparse
import urllib
from zipfile import ZipFile

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--training-endpoint", help="Training endpoint for Custom Vision", required=True)
parser.add_argument("--training-key", help="Training key for Custom Vision", required=True)
parser.add_argument("--data_path", type=str, default="./localdata", help="Dataset location")
args = parser.parse_args()

print(f"Using training endpoint {args.training_endpoint}, training key {args.training_key}, data path {args.data_path}")

# Download data
dir = args.data_path
url = "https://tkubicastore.blob.core.windows.net/datasets/IntelImageClassification-train.zip?sp=r&st=2023-01-10T08:07:34Z&se=2050-01-10T16:07:34Z&spr=https&sv=2021-06-08&sr=b&sig=NLeEHjOJWP8axxa%2F5tRgFbheFPjug7ZjV4NW9COlJWQ%3D"
os.makedirs(dir, exist_ok=True)
print(f"Downloading data from {url}")
dataset_name = "custom_vision_intel_image_classification"
dataset_dir = os.path.join(dir, dataset_name)

urllib.request.urlretrieve(url, filename="data.zip")

with ZipFile("data.zip", "r") as zip:
    print("Extracting files")
    zip.extractall(path=dataset_dir)
    print("Extraction complete")
os.remove("data.zip")

# Custom Vision training client
print("Getting client")
credentials = ApiKeyCredentials(in_headers={"Training-key": args.training_key})
trainer = CustomVisionTrainingClient(args.training_endpoint, credentials)

# Create a new project
print ("Creating project")
project = trainer.create_project("intel_image_classification", classification_type="Multiclass", domain_id="2e37d7fb-3a54-486a-b4d6-cfc369af0018")	

# Upload images - each class in a separate folder
dataset_base_dir = os.path.join(dataset_dir, os.listdir(dataset_dir)[0])
for class_name in os.listdir(dataset_base_dir):
    sub_dir = os.path.join(dataset_base_dir, class_name)
    if not os.path.isdir(sub_dir):
        continue

    print(f"\n\nProcessing {sub_dir}")
    print(f"Creating tag {class_name}")
    tag = trainer.create_tag(project.id, class_name)
    print(f"Uploading images for tag {class_name}")
    for image in os.listdir(sub_dir):
        trainer.create_images_from_data(project.id, open(os.path.join(sub_dir, image), "rb").read(), [tag.id])