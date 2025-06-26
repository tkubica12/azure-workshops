#!/usr/bin/env python3
"""
Train BERT model for sentiment analysis.
Uses the full training dataset with train/validation split.
Automatically uses GPU if available, falls back to CPU.
"""
import os
import sys
import logging
import argparse
from pathlib import Path
from dotenv import load_dotenv
from utils.bert_utils import BertUtils
from utils.data_utils import DataUtils
import pandas as pd
import json

# Load environment variables
load_dotenv()

# Set up logging
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO), 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def save_training_report(training_summary: dict, output_file: str):
    """Save training summary to file."""
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Create human-readable report
    report_lines = [
        "=" * 70,
        "BERT SENTIMENT ANALYSIS TRAINING REPORT",
        "=" * 70,
        f"Training completed: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "MODEL CONFIGURATION:",
        f"  Base Model: {training_summary['model_name']}",
        f"  Training Samples: {training_summary['training_samples']:,}",
        f"  Validation Samples: {training_summary['validation_samples']:,}",
        f"  Epochs: {training_summary['epochs']}",
        f"  Batch Size: {training_summary['batch_size']}",
        f"  Learning Rate: {training_summary['learning_rate']}",
        "",
        "TRAINING RESULTS:",
        f"  Training Time: {training_summary['training_time_minutes']:.2f} minutes",
        f"  Final Training Loss: {training_summary['final_train_loss']:.4f}",
        f"  Final Validation Accuracy: {training_summary['final_eval_accuracy']:.4f}",
        f"  Final Validation Loss: {training_summary['final_eval_loss']:.4f}",
        "",
        "HARDWARE INFO:",
        f"  Device: {training_summary['device_info']['device']}",
        f"  CPU Cores: {training_summary['device_info']['cpu_count']}",
        f"  System Memory: {training_summary['device_info']['memory_gb']} GB",
    ]
    
    if 'gpu_name' in training_summary['device_info']:
        report_lines.extend([
            f"  GPU: {training_summary['device_info']['gpu_name']}",
            f"  GPU Memory: {training_summary['device_info']['gpu_memory_gb']} GB",
            f"  CUDA Version: {training_summary['device_info']['cuda_version']}",
        ])
    
    report_lines.extend([
        "",
        f"Model saved to: {training_summary['output_dir']}",
        "=" * 70,
    ])
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    # Also save JSON version for programmatic access
    json_file = output_file.replace('.txt', '_summary.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(training_summary, f, indent=2, default=str)
    
    logger.info(f"Training report saved to: {output_file}")
    logger.info(f"Training summary saved to: {json_file}")


def main():
    """Main function to train BERT sentiment analysis model."""
    parser = argparse.ArgumentParser(
        description="Train BERT model for sentiment analysis"
    )
    parser.add_argument(
        "--train-file", 
        default="train/train_all.csv",
        help="Path to training CSV file (default: train/train_all.csv)"
    )
    parser.add_argument(
        "--model-name", 
        default="bert-base-uncased",
        help="Pre-trained model name (default: bert-base-uncased)"
    )
    parser.add_argument(
        "--output-dir", 
        default="models/bert_sentiment",
        help="Output directory for trained model (default: models/bert_sentiment)"
    )
    parser.add_argument(
        "--epochs", 
        type=int, 
        default=5,
        help="Number of training epochs (default: 5)"
    )
    parser.add_argument(
        "--batch-size", 
        type=int, 
        default=16,
        help="Training batch size (default: 16)"
    )
    parser.add_argument(
        "--learning-rate", 
        type=float, 
        default=2e-5,
        help="Learning rate (default: 2e-5)"
    )
    parser.add_argument(
        "--max-length", 
        type=int, 
        default=128,
        help="Maximum sequence length (default: 128)"
    )
    parser.add_argument(
        "--test-size", 
        type=float, 
        default=0.2,
        help="Validation split ratio (default: 0.2)"
    )
    
    args = parser.parse_args()
    
    logger.info("Starting BERT sentiment analysis training")
    logger.info(f"Training file: {args.train_file}")
    logger.info(f"Model: {args.model_name}")
    logger.info(f"Output directory: {args.output_dir}")
    
    try:
        # Load training data
        if not Path(args.train_file).exists():
            raise FileNotFoundError(f"Training file not found: {args.train_file}")
        
        logger.info(f"Loading training data from {args.train_file}")
        df = pd.read_csv(args.train_file)
        
        # Validate data
        required_columns = ['text', 'label']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        logger.info(f"Loaded {len(df):,} training samples")
        
        # Check label distribution
        label_counts = df['label'].value_counts().sort_index()
        logger.info("Label distribution:")
        for label, count in label_counts.items():
            logger.info(f"  Label {label}: {count:,} samples ({count/len(df)*100:.1f}%)")
        
        # Initialize BERT utilities
        bert_utils = BertUtils(
            model_name=args.model_name,
            num_labels=len(df['label'].unique()),
            max_length=args.max_length
        )
        
        # Load model and tokenizer
        bert_utils.load_model_and_tokenizer()
        
        # Prepare datasets
        logger.info("Preparing datasets...")
        train_dataset, val_dataset = bert_utils.prepare_dataset(df, test_size=args.test_size)
        
        # Train model
        logger.info("Starting model training...")
        training_summary = bert_utils.train_model(
            train_dataset=train_dataset,
            val_dataset=val_dataset,
            output_dir=args.output_dir,
            epochs=args.epochs,
            batch_size=args.batch_size,
            learning_rate=args.learning_rate
        )
        
        # Save training report
        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)
        
        report_file = results_dir / f"bert_training_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt"
        save_training_report(training_summary, str(report_file))
        
        # Print summary to console
        print("\n" + "=" * 70)
        print("BERT TRAINING COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print(f"Training Time: {training_summary['training_time_minutes']:.2f} minutes")
        print(f"Final Validation Accuracy: {training_summary['final_eval_accuracy']:.4f}")
        print(f"Model saved to: {training_summary['output_dir']}")
        print(f"Report saved to: {report_file}")
        print("=" * 70)
        
        logger.info("BERT training completed successfully!")
        
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
