import tiktoken

# Set the path to the input file
input_file_path = "../../inputs/european_wholesale_electricity_price_data_daily.csv" 

# Read the file content
with open(input_file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Use tiktoken for gpt-4.1 encoding
encoding = tiktoken.get_encoding("o200k_base")

tokens = encoding.encode(text)
print(f"Token count: {len(tokens)}")
