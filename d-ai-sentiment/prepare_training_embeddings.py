#!/usr/bin/env python3
"""
Script to prepare training embeddings from sentiment analysis training files.
Processes train_100.csv, train_1000.csv and train_all.csv to generate embeddings
using Azure OpenAI text-embedding-3-small model.
"""

import os
import sys
import time
import logging
from pathlib import Path

# Add utils directory to path for imports
sys.path.append(str(Path(__file__).parent / "utils"))

try:
    import pandas as pd
except ImportError:
    print("pandas is required. Install with: pip install pandas")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("python-dotenv is required. Install with: pip install python-dotenv")
    sys.exit(1)

try:
    from utils.llm_utils import LlmUtils
    from utils.data_utils import DataUtils
except ImportError as e:
    print(f"Error importing utils: {e}")
    print("Make sure you're running this script from the d-ai-sentiment directory")
    sys.exit(1)

# Load environment variables first
load_dotenv()

# Set up logging with configurable level from environment
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO), 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_training_file(file_path: str) -> pd.DataFrame:
    """Load training CSV file and return DataFrame."""
    try:
        df = pd.read_csv(file_path)
        logger.debug(f"Loaded {len(df)} samples from {file_path}")
        return df
    except Exception as e:
        logger.error(f"Error loading file {file_path}: {e}")
        raise

def create_embeddings_for_file(input_file: str, output_file: str, llm_utils: LlmUtils):
    """
    Process a single training file to create embeddings.
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file with embeddings
        llm_utils: LlmUtils instance for generating embeddings
          Returns:
        Summary statistics dictionary
    """
    file_start_time = time.time()
    logger.info(f"Processing {Path(input_file).name}...")
    print(f"\n🔄 Starting processing of {Path(input_file).name}...")
    
    # Load the training file
    df = load_training_file(input_file)
    
    # Extract texts and labels
    texts = df['text'].tolist()
    labels = df['label'].tolist()
    total_texts = len(texts)
    
    logger.info(f"Generating embeddings for {total_texts:,} texts...")
    print(f"📊 Generating embeddings for {total_texts:,} texts...")
    
    # Generate embeddings - process one text at a time for better error handling
    embeddings = []
    failed_count = 0
    
    for i, text in enumerate(texts):
        # Progress logging every 25% or every 100 items (whichever is less frequent)
        progress_interval = max(25, total_texts // 4)
        if i > 0 and (i % progress_interval == 0 or i == total_texts - 1):
            elapsed = time.time() - file_start_time
            rate = i / elapsed if elapsed > 0 else 0
            remaining = (total_texts - i) / rate if rate > 0 else 0
            logger.info(f"Progress: {i:,}/{total_texts:,} ({i/total_texts*100:.1f}%) | Rate: {rate:.1f}/s | ETA: {remaining:.0f}s")
        
        # Show progress every 100 records using print (more visible)
        if i > 0 and i % 100 == 0:
            elapsed = time.time() - file_start_time
            rate = i / elapsed if elapsed > 0 else 0
            print(f"  Processing: {i:,}/{total_texts:,} ({i/total_texts*100:.1f}%) - {rate:.1f} texts/sec")
        
        embedding_result = llm_utils.embed_text([text])
        if embedding_result and embedding_result[0] is not None:
            embeddings.append(embedding_result[0])
        else:
            logger.warning(f"Failed to generate embedding for text {i+1}, using zeros")
            failed_count += 1
            # Use zero vector as fallback (assuming 1536 dimensions for text-embedding-3-small)
            embeddings.append([0.0] * 1536)
      # Create output DataFrame with embeddings as a single array column
    # This is much more efficient than 1536 separate columns
    embedding_df = pd.DataFrame({
        'text': texts,
        'embedding': embeddings,  # Store as list/array
        'label': labels
    })
    
    # Save to Parquet format (much more efficient than CSV)
    embedding_df.to_parquet(output_file, index=False, compression='snappy')
    
    # Get file size for reporting
    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
      # Calculate processing time
    processing_time = time.time() - file_start_time
    embedding_dim = len(embeddings[0]) if embeddings else 1536
    
    # Print completion message
    print(f"✅ Completed {Path(input_file).name} in {processing_time:.1f}s")
    print(f"   → Saved {len(embedding_df):,} embeddings to {Path(output_file).name} ({file_size_mb:.2f} MB)")
    print(f"   → Embedding dimensions: {embedding_dim}")
    
    # Return summary statistics
    return {
        'input_file': Path(input_file).name,
        'output_file': Path(output_file).name,
        'total_texts': total_texts,
        'embedding_dim': embedding_dim,
        'failed_embeddings': failed_count,
        'success_rate': (total_texts - failed_count) / total_texts * 100,
        'processing_time': processing_time,
        'rate': total_texts / processing_time if processing_time > 0 else 0,
        'file_size_mb': file_size_mb
    }

def main():
    """Main function to process all training files."""
    script_start_time = time.time()
      # Define input and output file mappings
    train_dir = Path("train")
    files_to_process = {
        "train_100.csv": "train_embeddings_100.parquet",
        "train_1000.csv": "train_embeddings_1000.parquet", 
        "train_all.csv": "train_embeddings_all.parquet"
    }
    
    logger.info("Starting training embedding generation")
    logger.info("="*60)
    
    # Check if train directory exists
    if not train_dir.exists():
        logger.error(f"Train directory {train_dir} does not exist!")
        return
    
    # Initialize LLM utils for embedding generation
    try:
        logger.info("Initializing Azure OpenAI client...")
        llm_utils = LlmUtils()
        llm_utils.pre_authenticate()
        logger.info("Azure OpenAI client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Azure OpenAI client: {e}")
        return
    
    # Process each file
    processing_results = []
    total_files = len([f for f in files_to_process.keys() if (train_dir / f).exists()])
    processed_files = 0
    
    for input_filename, output_filename in files_to_process.items():
        input_path = train_dir / input_filename
        output_path = train_dir / output_filename
        
        # Check if input file exists
        if not input_path.exists():
            logger.warning(f"Input file {input_filename} not found, skipping...")
            continue
        
        # Check if output file already exists
        if output_path.exists():
            logger.warning(f"Output file {output_filename} already exists")
            response = input(f"Overwrite {output_filename}? (y/N): ")
            if response.lower() != 'y':
                logger.info(f"Skipping {input_filename}")
                continue
        
        try:
            # Process the file
            file_stats = create_embeddings_for_file(str(input_path), str(output_path), llm_utils)
            processing_results.append(file_stats)
            processed_files += 1
            
            # Log file completion
            logger.info(f"✓ Completed {input_filename} ({processed_files}/{total_files})")
            logger.info(f"  Success rate: {file_stats['success_rate']:.1f}%")
            logger.info(f"  Processing time: {file_stats['processing_time']:.1f}s")
            logger.info(f"  Rate: {file_stats['rate']:.1f} texts/sec")
            
        except Exception as e:
            logger.error(f"✗ Failed to process {input_filename}: {e}")
            continue
    
    # Generate final summary
    script_time = time.time() - script_start_time
    token_usage = llm_utils.get_token_usage()
    
    logger.info("="*60)
    logger.info("EMBEDDING GENERATION SUMMARY")
    logger.info("="*60)
    
    if processing_results:
        total_texts = sum(r['total_texts'] for r in processing_results)
        total_failed = sum(r['failed_embeddings'] for r in processing_results)
        avg_success_rate = sum(r['success_rate'] for r in processing_results) / len(processing_results)
        
        logger.info(f"Files processed: {len(processing_results)}/{total_files}")
        logger.info(f"Total texts: {total_texts:,}")
        logger.info(f"Failed embeddings: {total_failed:,}")
        logger.info(f"Average success rate: {avg_success_rate:.1f}%")
        logger.info("")
          # Per-file summary
        total_file_size = sum(r['file_size_mb'] for r in processing_results)
        for result in processing_results:
            logger.info(f"{result['input_file']:15} -> {result['output_file']:23} "
                       f"({result['total_texts']:,} texts, {result['file_size_mb']:.2f} MB, {result['success_rate']:.1f}% success)")
        
        logger.info(f"Total output size: {total_file_size:.2f} MB")
        logger.info("")
    
    # Token usage and cost estimation
    logger.info(f"API Statistics:")
    logger.info(f"  Total requests: {token_usage['total_requests']:,}")
    logger.info(f"  Total input tokens: {token_usage['total_input_tokens']:,}")
    
    # Calculate estimated cost (text-embedding-3-small: ~$0.00002 per 1K tokens)
    cost_per_1k_tokens = 0.00002
    estimated_cost = (token_usage['total_input_tokens'] / 1000) * cost_per_1k_tokens
    logger.info(f"  Estimated cost: ${estimated_cost:.6f}")
    
    logger.info(f"Total execution time: {script_time:.1f}s")
    logger.info("Embedding generation complete!")

if __name__ == "__main__":
    main()
