import tiktoken

# Set the path to the input and output files
input_file_path = "../../inputs/european_wholesale_electricity_price_data_daily.csv"
output_file_path = "../../inputs/european_wholesale_electricity_price_data_daily_100k.csv"
max_tokens = 100000

encoding = tiktoken.get_encoding("o200k_base")

token_count = 0
lines = []

with open(input_file_path, "r", encoding="utf-8") as infile:
    for line in infile:
        line_tokens = len(encoding.encode(line))
        if token_count + line_tokens > max_tokens:
            break
        lines.append(line)
        token_count += line_tokens

with open(output_file_path, "w", encoding="utf-8") as outfile:
    outfile.writelines(lines)

print(f"Wrote {len(lines)} lines and {token_count} tokens to {output_file_path}")
