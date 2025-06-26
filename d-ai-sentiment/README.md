# Sentiment Analysis Approach Comparison

A comprehensive experimental comparison of different approaches to sentiment analysis, evaluating Large Language Models (LLMs), fine-tuned models, embedding-based methods, and transformer architectures across accuracy, cost, and performance metrics.

## 🎯 Purpose

This project systematically compares 14 different sentiment analysis approaches to help practitioners choose the optimal method based on their specific requirements:

- **Accuracy requirements** (60.9% - 80.0% range observed)
- **Cost constraints** ($0.0005 - $10.67 per 1K samples)
- **Processing speed needs** (0.09 - 3.00 seconds per sample)
- **Infrastructure preferences** (cloud APIs vs local deployment)
- **Data privacy requirements**

## 🧪 Approaches Tested

### 1. Large Language Model (LLM) Approaches
- **GPT-4.1-nano**: Zero-shot, few-shot (100/1000 examples)
- **GPT-4.1-mini**: Zero-shot, few-shot (100/1000 examples)

### 2. Fine-tuned LLM Approaches  
- **GPT-4.1-nano Fine-tuned**: Zero-shot, few-shot (100 examples)
- **GPT-4.1-mini Fine-tuned**: Zero-shot, few-shot (100 examples)

### 3. Embedding + Machine Learning Approaches
- **OpenAI Embeddings + Logistic Regression**: Trained on 100, 1000, and full dataset

### 4. Fine-tuned Transformer Approaches
- **BERT-base Fine-tuned**: Traditional encoder-only transformer model

## 📁 Project Structure

```
d-ai-sentiment/
├── README.md                     # This file
├── config.yaml                   # Configuration settings
├── pyproject.toml               # Python dependencies
├── 
├── dataset/                     # Dataset files
│   ├── train_df.csv            # Training data
│   ├── val_df.csv              # Validation data
│   ├── test_df.csv             # Test data
│   └── README.md               # Dataset documentation
├── 
├── results/                     # Experiment results and analysis
│   ├── README.md               # 📊 COMPREHENSIVE RESULTS ANALYSIS
│   ├── *_results_*.csv         # Individual experiment results
│   ├── *_results_*.txt         # Detailed experiment reports
│   └── *_training_*.txt        # Training logs and statistics
├── 
├── models/                      # Trained model artifacts
├── train/                       # Training utilities
├── utils/                       # Helper functions
├── 
├── LLM experiment scripts:
├── llm_nano_zeroshot.py        # GPT-4.1-nano zero-shot
├── llm_nano_fewshot_100.py     # GPT-4.1-nano few-shot (100)
├── llm_nano_fewshot_1000.py    # GPT-4.1-nano few-shot (1000)
├── llm_mini_zeroshot.py        # GPT-4.1-mini zero-shot
├── llm_mini_fewshot_100.py     # GPT-4.1-mini few-shot (100)
├── llm_mini_fewshot_1000.py    # GPT-4.1-mini few-shot (1000)
├── llm_ft_nano_zeroshot.py     # Fine-tuned nano zero-shot
├── llm_ft_nano_fewshot_100.py  # Fine-tuned nano few-shot (100)
├── llm_ft_mini_zeroshot.py     # Fine-tuned mini zero-shot
├── llm_ft_mini_fewshot_100.py  # Fine-tuned mini few-shot (100)
├── 
├── ML experiment scripts:
├── train_lr_100.py             # Train LR with 100 samples
├── train_lr_1000.py            # Train LR with 1000 samples  
├── train_lr_all.py             # Train LR with full dataset
├── test_lr_100.py              # Test LR 100 model
├── test_lr_1000.py             # Test LR 1000 model
├── test_lr_all.py              # Test LR full model
├── 
├── BERT experiment scripts:
├── train_bert.py               # Train BERT model
├── train_bert_full.py          # Full BERT training pipeline
├── test_bert.py                # Test BERT model
└── 
└── Data preparation:
    ├── prepare_training_files.py   # Prepare fine-tuning data
    ├── prepare_training_embeddings.py # Generate embeddings
    ├── dataset_stats.py           # Dataset analysis
    └── dataset_trim.py            # Dataset trimming utilities
```

## 🏆 Key Results Summary

| Approach Category | Best Method | Accuracy | Cost per 1K | Speed | Key Advantage |
|------------------|-------------|----------|-------------|-------|---------------|
| **Overall Winner** | LR_ALL | 73.2% | $0.0005 | 5.58/sec | Best cost-effectiveness |
| **Highest Accuracy** | LLM_FT_MINI_ZEROSHOT | 80.0% | $0.202 | 3.30/sec | Maximum accuracy |
| **Fastest Processing** | BERT_SENTIMENT | 74.5% | $0.028 | 11.19/sec | Local inference speed |
| **Best Balance** | BERT_SENTIMENT | 74.5% | $0.028 | 11.19/sec | Accuracy + speed + privacy |

### Cost-Effectiveness Ranking
1. **Embedding+ML approaches**: $0.0005 per 1K samples (50-21,000x more cost-effective)
2. **LLM base models**: $0.025-$0.106 per 1K samples  
3. **BERT**: $0.028 per 1K samples (excellent accuracy-to-cost ratio)
4. **Fine-tuned LLMs**: $0.050-$0.202 per 1K samples (highest accuracy)

## 🎯 Quick Recommendations

### Choose Based on Your Priority:

- **💰 Cost-Sensitive**: Use **LR_ALL** ($0.0005/1K, 73.2% accuracy)
- **🎯 Maximum Accuracy**: Use **LLM_FT_MINI_ZEROSHOT** ($0.202/1K, 80.0% accuracy)  
- **⚡ Speed + Accuracy**: Use **BERT_SENTIMENT** ($0.028/1K, 74.5% accuracy, 11.19/sec)
- **🔒 Data Privacy**: Use **BERT_SENTIMENT** (local deployment, no external APIs)
- **🚀 Rapid Prototyping**: Use **LLM_NANO_ZEROSHOT** (no training required, 67.7% accuracy)

## 📊 Detailed Analysis

For comprehensive results including:
- Detailed performance metrics by sentiment class
- Cost analysis with caching considerations  
- Processing speed comparisons
- Technical methodology explanations
- Production deployment recommendations
- Break-even analysis for different approaches

**➡️ See the complete analysis: [results/README.md](results/README.md)**

## 📈 Dataset

Multi-class sentiment analysis dataset with:
- **Training**: 24,985 samples
- **Validation**: 6,247 samples  
- **Test**: 5,205 samples
- **Classes**: Negative (0), Neutral (1), Positive (2)

See [dataset/README.md](dataset/README.md) for detailed dataset information.