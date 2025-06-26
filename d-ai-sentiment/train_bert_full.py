#!/usr/bin/env python3
"""
Train BERT model for sentiment analysis with optimized default parameters.
This script uses the full training dataset and good defaults for best results.
Simply run: uv run python train_bert_full.py
"""
import subprocess
import sys
from pathlib import Path

def main():
    """Run BERT training with optimized defaults."""
    
    # Check if training file exists
    train_file = Path("train/train_all.csv")
    if not train_file.exists():
        print(f"❌ Error: Training file not found at {train_file}")
        print("Please ensure the training data is available.")
        return 1
    
    print("🚀 Starting BERT sentiment analysis training with optimized parameters...")
    print(f"📊 Training file: {train_file}")
    print(f"📝 Total samples: ~31,000")
    print(f"🎯 Training strategy: Fine-tuning BERT-base-uncased")
    print(f"⚡ Hardware: Using GPU if available")
    print(f"📈 Features: Early stopping, validation monitoring")
    print("-" * 60)
    
    # Optimized training parameters
    cmd = [
        sys.executable, "train_bert.py",
        "--train-file", "train/train_all.csv",
        "--model-name", "bert-base-uncased", 
        "--output-dir", "models/bert_sentiment_full",
        "--epochs", "5",                    # Enough epochs with early stopping
        "--batch-size", "16",               # Good balance for RTX 4060
        "--learning-rate", "2e-5",          # Standard BERT fine-tuning LR
        "--max-length", "128",              # Handle most tweets/short texts
        "--test-size", "0.2"                # 20% for validation
    ]
    
    try:
        # Run the training
        result = subprocess.run(cmd, check=True)
        
        print("\n" + "=" * 60)
        print("✅ BERT TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("📁 Model saved to: models/bert_sentiment_full/")
        print("📊 Report saved to: results/")
        print("🧪 Ready for testing with test_bert.py")
        print("=" * 60)
        
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Training failed with exit code {e.returncode}")
        return e.returncode
    except KeyboardInterrupt:
        print(f"\n⚠️  Training interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
