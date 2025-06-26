#!/usr/bin/env python3
"""
Train logistic regression model on 1000 embedding samples.
Uses GPU acceleration when available, falls back to CPU.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from utils.training_utils import TrainingUtils

# Load environment variables
load_dotenv()

# Set up logging
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO), 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main function to train logistic regression on 1000 embedding samples."""
    logger.info("Starting logistic regression training for 1000 samples")
    
    # Define paths
    data_path = "train/train_embeddings_1000.parquet"
    model_output_path = "models/lr_model_1000.pkl"
    stats_output_path = "results/lr_training_stats_1000.txt"
    
    # Check if data file exists
    if not os.path.exists(data_path):
        logger.error(f"Training data not found: {data_path}")
        print(f"❌ Error: Training data not found at {data_path}")
        print("Please run prepare_training_embeddings.py first to generate embedding files.")
        return
    
    try:
        # Initialize training utilities
        trainer = TrainingUtils(
            random_state=42,
            test_size=0.2,
            use_gpu=True,  # Will automatically fallback to CPU if GPU not available
            max_iter=1000
        )
        
        # Train the model (initial info and summary handled by TrainingUtils)
        results = trainer.train_model(
            data_path=data_path,
            model_output_path=model_output_path,
            stats_output_path=stats_output_path
        )
        
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        print(f"❌ Training failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
