# Classic sentiment analysis using LLMs or embeddings
This repo aims to compare different ways to achieve simple sentiment analysis:
- **BERT Fine-tuning**: Fine-tune BERT-base-uncased on sentiment classification
- **LLM zero-shot classification**: Use GPT models without examples
- **LLM in-context learning classification**: Use GPT models with few-shot examples
- **LLM fine-tuning classification**: Use fine-tuned GPT models
- **Embeddings + ML models**: Use OpenAI embeddings with logistic regression classifiers

## Quick Start

### BERT Training
Train a BERT model for sentiment analysis:
```bash
# Quick training with optimized defaults
uv run python train_bert_full.py

# Or custom training with specific parameters
uv run python train_bert.py --epochs 3 --batch-size 8
```

### BERT Testing  
Test the trained BERT model:
```bash
uv run python test_bert.py
```

### Other Approaches
See the various `llm_*.py` and `test_lr_*.py` scripts for other approaches.