import pandas as pd
import tiktoken
from typing import Dict, List, Tuple
import os


class DataUtils:
    """Utility class for calculating dataset statistics and token counts."""
    def __init__(self):
        """Initialize the calculator with tokenizers."""
        self.tokenizers = {
            'gpt41': tiktoken.encoding_for_model("gpt-4o"),  
            'embeddings': tiktoken.encoding_for_model("text-embedding-ada-002")
        }
    
    def load_csv_file(self, filepath: str) -> pd.DataFrame:
        """
        Load a CSV file and return as DataFrame.
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            pandas.DataFrame: Loaded data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            Exception: For other loading errors
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        try:
            df = pd.read_csv(filepath)
            return df
        except Exception as e:
            raise Exception(f"Error loading {filepath}: {str(e)}")
    
    def count_tokens(self, text: str, tokenizer_name: str) -> int:
        """
        Count tokens in text using specified tokenizer.
        
        Args:
            text: Text to tokenize
            tokenizer_name: Name of tokenizer ('gpt4' or 'embeddings')
            
        Returns:
            int: Number of tokens
        """
        if tokenizer_name not in self.tokenizers:
            raise ValueError(f"Unknown tokenizer: {tokenizer_name}")
        
        if pd.isna(text) or text == "":
            return 0
            
        return len(self.tokenizers[tokenizer_name].encode(str(text)))
    
    def calculate_dataset_stats(self, df: pd.DataFrame, text_column: str) -> Dict:
        """
        Calculate comprehensive statistics for a dataset.
        
        Args:
            df: DataFrame containing the data
            text_column: Name of column containing text data
            
        Returns:
            Dict: Statistics including record count and token statistics
        """
        if text_column not in df.columns:
            raise ValueError(f"Column '{text_column}' not found in dataset")
        
        stats = {
            'record_count': len(df),
            'text_column': text_column,
            'tokenizer_stats': {}
        }
        
        # Calculate token statistics for each tokenizer
        for tokenizer_name in self.tokenizers.keys():
            token_counts = df[text_column].apply(
                lambda x: self.count_tokens(x, tokenizer_name)
            )
            
            stats['tokenizer_stats'][tokenizer_name] = {
                'total_tokens': token_counts.sum(),
                'avg_tokens_per_record': token_counts.mean(),
                'min_tokens': token_counts.min(),
                'max_tokens': token_counts.max(),
                'median_tokens': token_counts.median()
            }
        
        return stats
    
    def format_stats_output(self, dataset_name: str, stats: Dict) -> str:
        """
        Format statistics for pretty printing.
        
        Args:
            dataset_name: Name of the dataset
            stats: Statistics dictionary from calculate_dataset_stats
            
        Returns:
            str: Formatted output string
        """
        output = [
            f"\n{'='*60}",
            f"DATASET STATISTICS: {dataset_name.upper()}",
            f"{'='*60}",
            f"Records: {stats['record_count']:,}",
            f"Text Column: '{stats['text_column']}'",
            ""
        ]
        for tokenizer_name, token_stats in stats['tokenizer_stats'].items():
            tokenizer_display = "GPT-4.1/GPT-4o Style" if tokenizer_name == 'gpt4' else "Embeddings Style"
            output.extend([
                f"{tokenizer_display} Tokenization:",
                f"  Total Tokens: {token_stats['total_tokens']:,}",
                f"  Average Tokens/Record: {token_stats['avg_tokens_per_record']:.2f}",
                f"  Min Tokens: {token_stats['min_tokens']:,}",
                f"  Max Tokens: {token_stats['max_tokens']:,}",
                f"  Median Tokens: {token_stats['median_tokens']:.0f}",
                ""
            ])
        
        return "\n".join(output)
    
    def get_label_distribution(self, df: pd.DataFrame, label_column: str = 'label') -> Dict:
        """
        Get the distribution of labels in the dataset.
        
        Args:
            df: DataFrame containing the data
            label_column: Name of the label column
            
        Returns:
            Dict: Label distribution statistics
        """
        if label_column not in df.columns:
            raise ValueError(f"Column '{label_column}' not found in dataset")
        
        label_counts = df[label_column].value_counts().sort_index()
        total_records = len(df)
        
        distribution = {
            'total_records': total_records,
            'label_counts': label_counts.to_dict(),
            'label_percentages': (label_counts / total_records * 100).round(2).to_dict()
        }
        
        return distribution
    
    def create_balanced_sample(self, df: pd.DataFrame, target_size: int, 
                              label_column: str = 'label', 
                              text_column: str = 'text',
                              random_state: int = 42) -> pd.DataFrame:
        """
        Create a balanced sample from the dataset with roughly equal representation
        of each label.
        
        Args:
            df: Source DataFrame
            target_size: Target number of records
            label_column: Name of the label column
            text_column: Name of the text column
            random_state: Random seed for reproducibility
            
        Returns:
            pd.DataFrame: Balanced sample with only text and label columns
        """
        if label_column not in df.columns or text_column not in df.columns:
            raise ValueError(f"Required columns '{text_column}' or '{label_column}' not found")
        
        # Get unique labels
        unique_labels = df[label_column].unique()
        records_per_label = target_size // len(unique_labels)
        remaining_records = target_size % len(unique_labels)
        
        sampled_dfs = []
        
        for i, label in enumerate(sorted(unique_labels)):
            label_df = df[df[label_column] == label]
            
            # Determine sample size for this label
            sample_size = records_per_label
            if i < remaining_records:  # Distribute remaining records to first few labels
                sample_size += 1
            
            # Sample records for this label
            if len(label_df) >= sample_size:
                sampled_label_df = label_df.sample(n=sample_size, random_state=random_state + i)
            else:
                # If not enough records, take all available
                sampled_label_df = label_df.copy()
                print(f"Warning: Only {len(label_df)} records available for label {label}, "
                      f"requested {sample_size}")
            
            sampled_dfs.append(sampled_label_df)
        
        # Combine all samples
        result_df = pd.concat(sampled_dfs, ignore_index=True)
        
        # Shuffle the final result
        result_df = result_df.sample(frac=1, random_state=random_state).reset_index(drop=True)
        
        # Return only text and label columns
        return result_df[[text_column, label_column]]
    
    def create_full_sample(self, df: pd.DataFrame, 
                          text_column: str = 'text',
                          label_column: str = 'label') -> pd.DataFrame:
        """
        Create a sample with all records but only text and label columns.
        
        Args:
            df: Source DataFrame
            text_column: Name of the text column
            label_column: Name of the label column
            
        Returns:
            pd.DataFrame: DataFrame with only text and label columns
        """
        if label_column not in df.columns or text_column not in df.columns:
            raise ValueError(f"Required columns '{text_column}' or '{label_column}' not found")
        
        return df[[text_column, label_column]].copy()
    
    def save_trimmed_dataset(self, df: pd.DataFrame, output_path: str) -> None:
        """
        Save trimmed dataset to CSV file.
        
        Args:
            df: DataFrame to save
            output_path: Output file path
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save to CSV
            df.to_csv(output_path, index=False)
            print(f"Saved {len(df)} records to {output_path}")
            
        except Exception as e:
            raise Exception(f"Error saving dataset to {output_path}: {str(e)}")
    
    def print_dataset_summary(self, df: pd.DataFrame, dataset_name: str, 
                             label_column: str = 'label') -> None:
        """
        Print a summary of the dataset including label distribution.
        
        Args:
            df: DataFrame to summarize
            dataset_name: Name of the dataset for display
            label_column: Name of the label column
        """
        distribution = self.get_label_distribution(df, label_column)
        
        print(f"\n{'='*50}")
        print(f"DATASET SUMMARY: {dataset_name}")
        print(f"{'='*50}")
        print(f"Total Records: {distribution['total_records']:,}")
        print(f"\nLabel Distribution:")
        
        for label, count in distribution['label_counts'].items():
            percentage = distribution['label_percentages'][label]
            print(f"  Label {label}: {count:,} records ({percentage}%)")

# ConfigLoader moved to config_utils.py for better organization
# Import it here for backward compatibility
from .config_utils import ConfigUtils as ConfigLoader
