#!/usr/bin/env python3
"""
Test BERT sentiment analysis model.
Loads the trained model and tests it on validation data.
Follows the same output format as other model testing scripts.
"""
import os
import sys
import logging
import argparse
from pathlib import Path
from dotenv import load_dotenv
from utils.bert_utils import BertUtils
from utils.analysis_utils import AnalysisUtils
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import json

# Load environment variables
load_dotenv()

# Set up logging
log_level = os.getenv('LOG_LEVEL', 'WARNING').upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.WARNING), 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Model configuration for consistent reporting
MODEL_CONFIG = {
    "deployment_name": "bert-base-uncased",
    "model_display_name": "BERT-base Sentiment",
    "input_cost_per_1k": 0.0,  # Local model, no API costs
    "output_cost_per_1k": 0.0,
    "api_version": "local"
}


def main():
    """Main function to test BERT sentiment analysis model."""
    parser = argparse.ArgumentParser(
        description="Test BERT sentiment analysis model"
    )
    parser.add_argument(
        "--model-path", 
        default="models/bert_sentiment",
        help="Path to trained BERT model (default: models/bert_sentiment_full)"
    )
    parser.add_argument(
        "--test-file", 
        default="dataset/val_df.csv",
        help="Path to test/validation CSV file (default: dataset/val_df.csv)"
    )
    parser.add_argument(
        "--output-file", 
        help="Custom output file name (default: auto-generated)"
    )
    
    args = parser.parse_args()
    
    logger.info("Starting BERT sentiment analysis testing")
    logger.info(f"Model path: {args.model_path}")
    logger.info(f"Test file: {args.test_file}")
    
    try:
        # Check if model exists
        if not Path(args.model_path).exists():
            raise FileNotFoundError(f"Model not found: {args.model_path}")
        
        # Load test data
        if not Path(args.test_file).exists():
            raise FileNotFoundError(f"Test file not found: {args.test_file}")
        
        logger.info(f"Loading test data from {args.test_file}")
        test_df = pd.read_csv(args.test_file)
        
        # Validate data
        required_columns = ['text', 'label']
        missing_columns = [col for col in required_columns if col not in test_df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        logger.info(f"Loaded {len(test_df):,} test samples")
        
        # Check label distribution
        label_counts = test_df['label'].value_counts().sort_index()
        logger.info("Test data label distribution:")
        for label, count in label_counts.items():
            logger.info(f"  Label {label}: {count:,} samples ({count/len(test_df)*100:.1f}%)")
        
        # Initialize BERT utilities
        bert_utils = BertUtils()
        
        # Load trained model
        logger.info("Loading trained BERT model...")
        bert_utils.load_model_and_tokenizer(args.model_path)
        
        # Initialize analysis utilities for consistent reporting
        analysis_utils = AnalysisUtils("bert_sentiment")
        
        # Create BERT classifier function that matches the expected interface
        def bert_classifier(text: str) -> int:
            """Classifier function that matches the interface expected by AnalysisUtils."""
            return bert_utils.predict_single(text)
        
        # Run the experiment using the same framework as other models
        results_df, report = analysis_utils.run_experiment(
            classifier_func=bert_classifier,
            data_path=args.test_file,
            llm_utils=None,  # No LLM utils for BERT
            model_config=MODEL_CONFIG,
            display_progress=True,
            display_interval=100
        )
        
        logger.info("BERT testing completed successfully!")
        
    except Exception as e:
        logger.error(f"Testing failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
