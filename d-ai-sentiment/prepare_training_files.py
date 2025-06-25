"""
Prepare JSONL files for model fine-tuning from sentiment analysis datasets.
"""

import pandas as pd
import json
import os
from pathlib import Path

def create_system_prompt():
    """
    Create the system prompt for sentiment classification (hardcoded from llm_utils.py).
    
    Returns:
        System prompt string
    """
    examples_csv = '''text,label
"I hate this app, it's terrible!",0
"The weather is cloudy today",1
"I love this new feature!",2'''
    
    prompt = f"""You are a sentiment analysis classifier. Your task is to classify text into one of three sentiment categories:

- 0: Negative sentiment (complaints, dissatisfaction, anger, sadness, frustration, etc.)
- 1: Neutral sentiment (factual statements, questions, neutral observations, mixed feelings, etc.)  
- 2: Positive sentiment (praise, satisfaction, happiness, excitement, love, etc.)

IMPORTANT RULES:
1. You must respond with ONLY a single digit: 0, 1, or 2
2. Do not include any text, explanation, or additional characters
3. Do not use quotes, spaces, or punctuation
4. Just return the number representing the sentiment class

EXAMPLES (in CSV format):
{examples_csv}

Based on these examples, classify the following text with the same approach.
Always return only the sentiment class as a single digit without any additional text."""
    
    return prompt

def prepare_jsonl_data(csv_file_path: str, output_file_path: str):
    """
    Convert CSV data to JSONL format for fine-tuning.
    
    Args:
        csv_file_path: Path to input CSV file
        output_file_path: Path to output JSONL file
    """
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Get the system prompt
    system_prompt = create_system_prompt()
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    
    # Prepare JSONL data
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            text = row['text']
            label = str(row['label'])  # Convert to string as required
            
            # Create the training example in the required format
            training_example = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Classify this text: {text}"},
                    {"role": "assistant", "content": label}
                ]
            }
            
            # Write as JSON line
            f.write(json.dumps(training_example, ensure_ascii=False) + '\n')
    
    print(f"Created {output_file_path} with {len(df)} examples")

def main():
    """Main function to prepare training and test files."""
    
    # Define paths
    base_dir = Path(__file__).parent
    dataset_dir = base_dir / "dataset"
    train_dir = base_dir / "train"
    
    # Input files
    train_csv = dataset_dir / "train_df.csv"
    test_csv = dataset_dir / "test_df.csv"
    
    # Output files
    train_jsonl = train_dir / "finetuning_train.jsonl"
    test_jsonl = train_dir / "finetuning_test.jsonl"
    
    # Check if input files exist
    if not train_csv.exists():
        raise FileNotFoundError(f"Training file not found: {train_csv}")
    
    if not test_csv.exists():
        raise FileNotFoundError(f"Test file not found: {test_csv}")
    
    # Prepare training data
    print("Preparing training data...")
    prepare_jsonl_data(str(train_csv), str(train_jsonl))
    
    # Prepare test data
    print("Preparing test data...")
    prepare_jsonl_data(str(test_csv), str(test_jsonl))
    
    print("Fine-tuning files preparation completed!")
    print(f"Training file: {train_jsonl}")
    print(f"Test file: {test_jsonl}")

if __name__ == "__main__":
    main()