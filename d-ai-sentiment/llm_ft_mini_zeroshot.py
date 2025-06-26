"""
Zero-shot sentiment analysis using Azure OpenAI fine-tuned GPT-4.1-mini.
"""

import os
import logging
from dotenv import load_dotenv
from utils.llm_utils import LlmUtils
from utils.analysis_utils import AnalysisUtils

# Load environment variables first
load_dotenv()

# Set up logging with configurable level from environment
log_level = os.getenv('LOG_LEVEL', 'WARNING').upper()
logging.basicConfig(level=getattr(logging, log_level, logging.WARNING), format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Model configuration
MODEL_CONFIG = {
    "deployment_name": "mini-2025-04-14-kubicasentiment",
    "api_version": "2024-12-01-preview",
    "input_cost_per_1k": 0.0004,  # $0.0004 per 1K input tokens for GPT-4.1-mini
    "output_cost_per_1k": 0.0016,  # $0.0016 per 1K output tokens for GPT-4.1-mini
    "model_display_name": "GPT-4.1-mini (Fine-tuned)"
}


def main():
    """Main function to run zero-shot sentiment analysis with fine-tuned GPT-4.1-mini."""
    try:
        # Load examples from train/default.csv
        examples_path = "train/default.csv"
        logger.info(f"Loading examples from {examples_path}")
        
        with open(examples_path, 'r', encoding='utf-8') as f:
            examples_csv = f.read().strip()
        
        logger.info(f"Loaded {len(examples_csv.splitlines())} lines from examples file")
        
        # Initialize LLM with examples and model config
        llm = LlmUtils(
            examples_csv=examples_csv,
            deployment_name=MODEL_CONFIG["deployment_name"],
            api_version=MODEL_CONFIG["api_version"]
        )
        logger.info(f"LLM client initialized successfully with {MODEL_CONFIG['model_display_name']}")
        
        # Pre-authenticate to warm up token cache
        llm.pre_authenticate()
        logger.info("Authentication completed")
        
        # Reset token usage counters to start fresh
        llm.reset_token_usage()
        
        # Initialize analysis utils
        analysis = AnalysisUtils(experiment_name="llm_ft_mini_zeroshot")
        
        # Run the experiment with built-in progress tracking
        results_df, report = analysis.run_experiment(
            classifier_func=llm.classify_sentiment,
            data_path="dataset/val_df.csv",
            llm_utils=llm,
            model_config=MODEL_CONFIG,
            display_progress=True,
            display_interval=100
        )
        
    except Exception as e:
        logger.error(f"Error during execution: {str(e)}")
        raise


if __name__ == "__main__":
    main()
