#!/usr/bin/env python3
"""
Test logistic regression model trained on 100 embedding samples.
Loads the trained model and tests it on validation data.
"""

import os
import logging
from dotenv import load_dotenv
from utils.llm_utils import LlmUtils
from utils.analysis_utils import AnalysisUtils
from utils.training_utils import TrainingUtils

# Load environment variables first
load_dotenv()

# Set up logging with configurable level from environment
log_level = os.getenv('LOG_LEVEL', 'WARNING').upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.WARNING), 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Model configuration
MODEL_CONFIG = {
    "model_type": "Logistic Regression",
    "training_samples": 100,
    "model_file": "models/lr_model_100.pkl",
    "embedding_model": "text-embedding-3-small",
    "input_cost_per_1k": 0.00002,  # Cost for embedding generation
    "output_cost_per_1k": 0.0,  
    "model_display_name": "LR-100"
}


def main():
    """Main function to test logistic regression model trained on 100 samples."""
    try:
        # Check if model file exists
        model_path = MODEL_CONFIG["model_file"]
        if not os.path.exists(model_path):
            logger.error(f"Model file not found: {model_path}")
            print(f"❌ Error: Model file not found at {model_path}")
            print("Please run train_lr_100.py first to train the model.")
            return
        
        # Initialize LLM utils for embedding generation (no examples needed for embeddings)
        llm = LlmUtils(
            embedding_deployment_name=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME", "text-embedding-3-small")
        )
        logger.info(f"LLM client initialized for embeddings with {MODEL_CONFIG['embedding_model']}")
        
        # Pre-authenticate to warm up token cache
        llm.pre_authenticate()
        logger.info("Authentication completed")
        
        # Reset token usage counters to start fresh
        llm.reset_token_usage()
        
        # Initialize training utilities and create classifier
        trainer = TrainingUtils()
        classifier_func = trainer.create_lr_classifier(model_path, llm)
        logger.info(f"Logistic regression classifier created from {model_path}")
        
        # Initialize analysis utils
        analysis = AnalysisUtils(experiment_name="test_lr_100")
        
        # Run the experiment with built-in progress tracking
        results_df, report = analysis.run_experiment(
            classifier_func=classifier_func,
            data_path="dataset/val_df.csv",
            llm_utils=llm,
            model_config=MODEL_CONFIG,
            display_progress=True,
            display_interval=100
        )
        
        logger.info("Test completed successfully")
        
    except Exception as e:
        logger.error(f"Error during execution: {str(e)}")
        print(f"❌ Test failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
