#!/usr/bin/env python3
"""
Dataset Trimming Script

This script creates trimmed versions of the training dataset with balanced
label distribution. Creates train_100.csv, train_1000.csv, and train_all.csv
in the train/ folder.

Usage:
    python dataset_trim.py [--config CONFIG_FILE] [--input INPUT_FILE] [--output-dir OUTPUT_DIR]
"""

import argparse
import sys
import os
from typing import Dict, List

# Add utils to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_utils import DataUtils
from utils.config_utils import ConfigUtils


def main():
    """Main function to run the dataset trimming."""
    parser = argparse.ArgumentParser(
        description="Create trimmed training datasets with balanced label distribution"
    )
    parser.add_argument(
        '--config', 
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    parser.add_argument(
        '--input',
        help='Input training file path (overrides config file)'
    )
    parser.add_argument(
        '--output-dir',
        default='train',
        help='Output directory for trimmed files (default: train)'
    )
    parser.add_argument(
        '--text-column',
        default='text',
        help='Name of text column (default: text)'
    )
    parser.add_argument(
        '--label-column',
        default='label',
        help='Name of label column (default: label)'
    )
    parser.add_argument(
        '--random-seed',
        type=int,
        default=42,
        help='Random seed for reproducibility (default: 42)'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize data utils
        data_utils = DataUtils()
        
        # Determine input file
        input_file = args.input
        if not input_file:
            try:
                # Try to load from config
                config = ConfigUtils.load_config(args.config)
                ConfigUtils.validate_dataset_config(config)
                input_file = config['dataset_files']['train']
                print(f"Using training file from config: {input_file}")
            except Exception as e:
                print(f"Error loading config: {e}")
                print("Please specify input file with --input option")
                sys.exit(1)
        else:
            print(f"Using specified input file: {input_file}")
        
        # Load the original training dataset
        print(f"\nLoading training dataset: {input_file}")
        train_df = data_utils.load_csv_file(input_file)
        
        # Display original dataset summary
        data_utils.print_dataset_summary(train_df, "ORIGINAL TRAINING", args.label_column)
        
        # Define trimming configurations
        trim_configs = [
            {'size': 100, 'filename': 'train_100.csv'},
            {'size': 1000, 'filename': 'train_1000.csv'},
            {'size': 'all', 'filename': 'train_all.csv'}
        ]
        
        # Create output directory
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Process each trimming configuration
        for config in trim_configs:
            size = config['size']
            filename = config['filename']
            output_path = os.path.join(args.output_dir, filename)
            
            print(f"\nCreating {filename}...")
            
            if size == 'all':
                # Create full sample with only text and label columns
                trimmed_df = data_utils.create_full_sample(
                    train_df, 
                    text_column=args.text_column,
                    label_column=args.label_column
                )
            else:
                # Create balanced sample
                trimmed_df = data_utils.create_balanced_sample(
                    train_df,
                    target_size=size,
                    text_column=args.text_column,
                    label_column=args.label_column,
                    random_state=args.random_seed
                )
            
            # Save the trimmed dataset
            data_utils.save_trimmed_dataset(trimmed_df, output_path)
            
            # Display summary
            data_utils.print_dataset_summary(trimmed_df, filename.upper(), args.label_column)
        
        print(f"\n{'='*60}")
        print("DATASET TRIMMING COMPLETED SUCCESSFULLY!")
        print(f"{'='*60}")
        print(f"Output directory: {args.output_dir}")
        print("Files created:")
        for config in trim_configs:
            output_path = os.path.join(args.output_dir, config['filename'])
            print(f"  - {output_path}")
        
        print(f"\nNote: Samples use random seed {args.random_seed} for reproducibility")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
