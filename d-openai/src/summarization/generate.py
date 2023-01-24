import os
import openai
import csv
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_URL")
openai.api_version = "2022-12-01"
openai.api_key = os.getenv("OPENAI_API_KEY")

# Exit if the environment variables are not set
if "OPENAI_API_URL" not in os.environ or "OPENAI_API_KEY" not in os.environ:
    raise Exception("Please set OPENAI_API_KEY and OPENAI_API_URL environment variable")

# Read input text file
with open("./text.txt", 'r') as f:
    prompt = f.read()

# Add the TL;DR to the prompt
prompt = prompt + "\n\nTL;DR"

# Define combinations of parameters to score
dataset = [
    {"temperature": 1, "top_p": 1, "frequency_penalty": 0, "presence_penalty": 0},
    {"temperature": 1, "top_p": 1, "frequency_penalty": 0, "presence_penalty": 0},
    {"temperature": 0, "top_p": 1, "frequency_penalty": 0, "presence_penalty": 0},
    {"temperature": 0, "top_p": 1, "frequency_penalty": 0, "presence_penalty": 0},
    {"temperature": 1, "top_p": 1, "frequency_penalty": 0, "presence_penalty": 0},
    {"temperature": 1, "top_p": 1, "frequency_penalty": 0, "presence_penalty": 0},
    {"temperature": 1, "top_p": 0, "frequency_penalty": 0, "presence_penalty": 0},
    {"temperature": 1, "top_p": 0, "frequency_penalty": 0, "presence_penalty": 0},
    {"temperature": 0, "top_p": 1, "frequency_penalty": 1, "presence_penalty": 0},
    {"temperature": 0, "top_p": 1, "frequency_penalty": 2, "presence_penalty": 0},
    {"temperature": 0, "top_p": 1, "frequency_penalty": 0, "presence_penalty": 1},
    {"temperature": 0, "top_p": 1, "frequency_penalty": 0, "presence_penalty": 2},
    {"temperature": 0.5, "top_p": 1, "frequency_penalty": 0.5, "presence_penalty": 0.2},
]

# Generate the responses
for data in dataset:
    print(f"Generating: temperature={data['temperature']}, top_p={data['top_p']}, frequency_penalty={data['frequency_penalty']}, presence_penalty={data['presence_penalty']}")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=data["temperature"],
        max_tokens=550,
        top_p=data["top_p"],
        frequency_penalty=data["frequency_penalty"],
        presence_penalty=data["presence_penalty"],
        stop=None)
    data["response"] = response.choices[0].text
    print(f"Response: {data['response']}\n\n")

# Write the output to CSV file
print("Writing output to CSV file")
headers = ["temperature", "top_p", "frequency_penalty", "presence_penalty", "response"]
with open("output.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(dataset)
