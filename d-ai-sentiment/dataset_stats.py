#!/usr/bin/env python3
"""
Dataset Statistics Calculator

This script analyzes CSV datasets and calculates token counts using different
tokenizers (GPT-4.1/GPT-4o style and OpenAI embeddings style).

Usage:
    python dataset_stats.py [--config CONFIG_FILE]
"""

import argparse
import sys
import os
from typing import Dict, List

# Add utils to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_utils import DataUtils
from utils.config_utils import ConfigUtils


def load_config(config_path: str) -> Dict:
    """
    Load configuration from file, trying YAML first, then simple format.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Dict: Configuration data
    """
    return ConfigUtils.load_config(config_path)


def validate_config(config: Dict) -> None:
    """
    Validate configuration structure.
    
    Args:
        config: Configuration dictionary
        
    Raises:
        ValueError: If configuration is invalid
    """
    ConfigUtils.validate_dataset_config(config)


def print_summary(all_stats: Dict[str, Dict]) -> None:
    """
    Print a summary comparison of all datasets.
    
    Args:
        all_stats: Dictionary containing stats for all datasets
    """
    print(f"\n{'='*60}")
    print("SUMMARY COMPARISON")
    print(f"{'='*60}")
    
    # Record counts
    print(f"{'Dataset':<12} {'Records':<12} {'GPT-4.1 Tokens':<15} {'Embed Tokens':<15}")
    print("-" * 60)
    
    total_records = 0
    total_gpt4_tokens = 0
    total_embed_tokens = 0
    
    for dataset_name, stats in all_stats.items():
        records = stats['record_count']
        gpt4_tokens = stats['tokenizer_stats']['gpt41']['total_tokens']
        embed_tokens = stats['tokenizer_stats']['embeddings']['total_tokens']
        
        print(f"{dataset_name:<12} {records:<12,} {gpt4_tokens:<15,} {embed_tokens:<15,}")
        
        total_records += records
        total_gpt4_tokens += gpt4_tokens
        total_embed_tokens += embed_tokens
    
    print("-" * 60)
    print(f"{'TOTAL':<12} {total_records:<12,} {total_gpt4_tokens:<15,} {total_embed_tokens:<15,}")


def main():
    """Main function to run the dataset statistics calculation."""
    parser = argparse.ArgumentParser(
        description="Calculate dataset statistics and token counts"
    )
    parser.add_argument(
        '--config', 
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        print(f"Loading configuration from: {args.config}")
        config = load_config(args.config)
        validate_config(config)
        
        # Initialize calculator
        data_utils = DataUtils()
        
        # Process each dataset
        all_stats = {}
        text_column = config['text_column']
        
        for dataset_name, filepath in config['dataset_files'].items():
            print(f"\nProcessing {dataset_name} dataset: {filepath}")
            
            try:
                # Load and analyze dataset
                df = data_utils.load_csv_file(filepath)
                stats = data_utils.calculate_dataset_stats(df, text_column)
                all_stats[dataset_name] = stats
                
                # Print formatted statistics
                formatted_output = data_utils.format_stats_output(dataset_name, stats)
                print(formatted_output)
                
            except Exception as e:
                print(f"Error processing {dataset_name} dataset: {e}")
                continue
        
        # Print summary if we have results
        if all_stats:
            print_summary(all_stats)
        else:
            print("No datasets were successfully processed.")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()