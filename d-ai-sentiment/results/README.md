# Sentiment Analysis Experiment Results

## Overview

This document presents the results of sentiment analysis experiments conducted on June 25-26, 2025, comparing different approaches:

1. **Large Language Models (LLMs)**: GPT-4.1-mini and GPT-4.1-nano with various prompting strategies (zero-shot, few-shot with 100/1000 examples)
2. **Fine-tuned Large Language Model Approaches**: Fine-tuned versions of GPT-4.1-mini and GPT-4.1-nano models trained on the full training dataset
3. **Hybrid Embedding + ML Models**: OpenAI embedding models combined with logistic regression classifiers trained on different dataset sizes (100, 1000, and full training set)
4. **Fine-tuned Transformer Approaches**: Traditional encoder-only transformer models (BERT) fine-tuned on the sentiment classification task

## Experiment Comparison Table

| Experiment | Model/Approach | Strategy | Accuracy | Completed Predictions | Failed Predictions | Total Tokens | Input Tokens | Output Tokens | Estimated Cost | Execution Time | Samples/sec |
|------------|---------------|----------|----------|---------------------|-------------------|--------------|--------------|---------------|----------------|----------------|-------------|
| **LLM Approaches** |
| LLM_NANO_ZEROSHOT | GPT-4.1-nano | Zero-shot | 67.7% | 5,166 (99.3%) | 39 (0.7%) | 1,289,946 | 1,284,780 | 5,166 | $0.13 | 3,306.7s | 1.56 |
| LLM_NANO_FEWSHOT_100 | GPT-4.1-nano | Few-shot (100) | 68.6% | 5,165 (99.2%) | 40 (0.8%) | 14,470,776 | 14,465,611 | 5,165 | $1.45 (~$0.87 cached) | 4,215.4s | 1.23 |
| LLM_NANO_FEWSHOT_1000 | GPT-4.1-nano | Few-shot (1000) | 68.4% | 5,166 (99.3%) | 39 (0.7%) | 133,890,834 | 133,885,668 | 5,166 | $13.39 (~$8.03 cached) | 9,160.4s | 0.56 |
| LLM_MINI_ZEROSHOT | GPT-4.1-mini | Zero-shot | 69.3% | 5,076 (97.5%) | 129 (2.5%) | 1,351,565 | 1,346,144 | 5,421 | $0.55 | 3,919.9s | 1.38 |
| LLM_MINI_FEWSHOT_100 | GPT-4.1-mini | Few-shot (100) | 69.4% | 5,140 (98.8%) | 65 (1.2%) | 14,688,863 | 14,683,620 | 5,243 | $5.88 (~$3.53 cached) | 5,565.6s | 0.94 |
| LLM_MINI_FEWSHOT_1000 | GPT-4.1-mini | Few-shot (1000) | 68.4% | 5,088 (97.8%) | 117 (2.2%) | 138,814,519 | 138,809,163 | 5,356 | $55.53 (~$33.32 cached) | 16,084.1s | 0.33 |
| **Fine-tuned LLM Approaches** |
| LLM_FT_NANO_ZEROSHOT | GPT-4.1-nano (Fine-tuned) | Zero-shot | 79.0% | 5,166 (99.3%) | 39 (0.7%) | 1,289,946 | 1,284,780 | 5,166 | $0.26 | 1,907.0s | 2.71 |
| LLM_FT_NANO_FEWSHOT_100 | GPT-4.1-nano (Fine-tuned) | Few-shot (100) | 78.4% | 5,166 (99.3%) | 39 (0.7%) | 14,473,578 | 14,468,412 | 5,166 | $2.90 (~$1.74 cached) | 1,940.0s | 2.66 |
| LLM_FT_MINI_ZEROSHOT | GPT-4.1-mini (Fine-tuned) | Zero-shot | 80.0% | 5,166 (99.3%) | 39 (0.7%) | 1,289,946 | 1,284,780 | 5,166 | $1.04 | 1,564.2s | 3.30 |
| LLM_FT_MINI_FEWSHOT_100 | GPT-4.1-mini (Fine-tuned) | Few-shot (100) | 79.3% | 5,165 (99.2%) | 40 (0.8%) | 14,470,685 | 14,465,520 | 5,165 | $11.58 (~$6.95 cached) | 1,918.4s | 2.69 |
| **Embedding + ML Approaches** |
| LR_100 | OpenAI Embeddings + LR | Trained on 100 samples | 60.9% | 5,205 (100%) | 0 (0%) | 124,123 | 124,123 | 0 | $0.0025 | 963.2s | 5.40 |
| LR_1000 | OpenAI Embeddings + LR | Trained on 1000 samples | 67.1% | 5,205 (100%) | 0 (0%) | 124,123 | 124,123 | 0 | $0.0025 | 951.7s | 5.47 |
| LR_ALL | OpenAI Embeddings + LR | Trained on full dataset | 73.2% | 5,205 (100%) | 0 (0%) | 124,123 | 124,123 | 0 | $0.0025 | 932.1s | 5.58 |
| **Fine-tuned Transformer Approaches** |
| BERT_SENTIMENT | BERT-base Fine-tuned | Trained on full dataset | 74.5% | 5,205 (100%) | 0 (0%) | N/A | N/A | N/A | $0.028 | 465.4s | 11.19 |

## Detailed Performance Metrics

### Accuracy by Sentiment Class

| Experiment | Negative Accuracy | Neutral Accuracy | Positive Accuracy |
|------------|------------------|------------------|-------------------|
| **LLM Approaches** |
| LLM_NANO_ZEROSHOT | 64.7% | 61.1% | 77.3% |
| LLM_NANO_FEWSHOT_100 | 62.9% | 73.0% | 68.6% |
| LLM_NANO_FEWSHOT_1000 | 74.2% | 57.9% | 74.7% |
| LLM_MINI_ZEROSHOT | 77.8% | 57.4% | 74.9% |
| LLM_MINI_FEWSHOT_100 | 74.6% | 60.3% | 74.9% |
| LLM_MINI_FEWSHOT_1000 | 71.7% | 59.9% | 74.8% |
| **Fine-tuned LLM Approaches** |
| LLM_FT_NANO_ZEROSHOT | 84.3% | 70.7% | 83.4% |
| LLM_FT_NANO_FEWSHOT_100 | 87.4% | 65.2% | 85.1% |
| LLM_FT_MINI_ZEROSHOT | 82.0% | 74.7% | 84.1% |
| LLM_FT_MINI_FEWSHOT_100 | 84.5% | 70.6% | 84.2% |
| **Embedding + ML Approaches** |
| LR_100 | 69.9% | 38.3% | 77.9% |
| LR_1000 | 74.2% | 55.0% | 74.1% |
| LR_ALL | 74.9% | 69.6% | 75.7% |
| **Fine-tuned Transformer Approaches** |
| BERT_SENTIMENT | 70.9% | 73.5% | 78.6% |

### Cost Analysis

| Experiment | Cost per 1K Samples | Cost Efficiency Rank |
|------------|-------------------|---------------------|
| **Most Cost-Effective** |
| LR_100 | $0.0005 | 1st (Best) |
| LR_1000 | $0.0005 | 1st (Best) |
| LR_ALL | $0.0005 | 1st (Best) |
| LLM_NANO_ZEROSHOT | $0.025 | 4th |
| BERT_SENTIMENT | $0.028 | 5th |
| LLM_FT_NANO_ZEROSHOT | $0.050 | 6th |
| LLM_MINI_ZEROSHOT | $0.106 | 7th |
| LLM_FT_MINI_ZEROSHOT | $0.202 | 8th |
| **Moderate Cost** |
| LLM_NANO_FEWSHOT_100 | $0.280 ($0.168 cached) | 9th |
| LLM_FT_NANO_FEWSHOT_100 | $0.562 ($0.337 cached) | 10th |
| LLM_MINI_FEWSHOT_100 | $1.130 ($0.678 cached) | 11th |
| LLM_FT_MINI_FEWSHOT_100 | $2.242 ($1.345 cached) | 12th |
| **High Cost** |
| LLM_NANO_FEWSHOT_1000 | $2.590 ($1.554 cached) | 13th |
| LLM_MINI_FEWSHOT_1000 | $10.670 ($6.402 cached) | 14th (Most Expensive) |

### Processing Speed Analysis

| Experiment | Processing Speed Rank | Time per Sample (seconds) |
|------------|---------------------|---------------------------|
| **Fastest Processing** |
| BERT_SENTIMENT | 1st (Fastest) | 0.09 |
| LR_ALL | 2nd | 0.18 |
| LR_1000 | 3rd | 0.18 |
| LR_100 | 4th | 0.19 |
| **Moderate Speed** |
| LLM_FT_MINI_ZEROSHOT | 5th | 0.30 |
| LLM_FT_MINI_FEWSHOT_100 | 6th | 0.37 |
| LLM_FT_NANO_ZEROSHOT | 7th | 0.37 |
| LLM_FT_NANO_FEWSHOT_100 | 8th | 0.38 |
| LLM_NANO_ZEROSHOT | 9th | 0.64 |
| LLM_MINI_ZEROSHOT | 10th | 0.72 |
| LLM_NANO_FEWSHOT_100 | 11th | 0.81 |
| LLM_MINI_FEWSHOT_100 | 12th | 1.06 |
| **Slower Processing** |
| LLM_NANO_FEWSHOT_1000 | 13th | 1.77 |
| LLM_MINI_FEWSHOT_1000 | 14th (Slowest) | 3.00 |

**Note**: BERT processing times represent fully local inference without network latency, while other approaches include network round-trip times to cloud APIs which can vary significantly based on location and network conditions.

## Technical Methodology

### Large Language Model (LLM) Approaches
Direct text-to-classification using GPT-4.1-mini and GPT-4.1-nano with various prompting strategies:
- **Zero-shot**: Direct classification without examples
- **Few-shot**: Classification with 100 or 1000 labeled examples in the prompt

**Cost considerations for few-shot approaches:**
- **Prompt caching**: OpenAI automatically applies 50% discount on cached input tokens (≥1,024 tokens)
- **Cache behavior**: Few-shot examples are likely cached after initial requests, reducing input token costs
- **Pricing in tables**: Standard (non-cached) pricing shown; actual costs may be ~30-40% lower due to caching

### Fine-tuned Large Language Model Approaches
Fine-tuned versions of GPT-4.1-mini and GPT-4.1-nano models trained on the full training dataset:
- **Fine-tuning process**: Models were fine-tuned on 7,848,000 tokens from the complete training dataset
- **Training cost**: $39.24 per model (both nano and mini)
- **Training duration**: 8h 20m for nano, 2h 25m for mini
- **Inference strategies**: Both zero-shot and few-shot (100 examples) approaches tested. Note with finetuned model adding examples increased cost while reducing accuracy so there is no point in using few-shot prompting with fine-tuned models unless there is some change in the task or domain.

**Pricing considerations:**
- **OpenAI pricing model (used in analysis)**: No hosting fees, but 2x token pricing compared to base models
- **Azure OpenAI alternative**: Same token pricing as base models but requires hourly hosting fees ($1.70/hour for mini, nano pricing TBD)

### Embedding + Machine Learning Approaches
Two-stage pipeline combining OpenAI embeddings with traditional ML:
1. **Text → Embeddings**: OpenAI's text embedding model converts text to high-dimensional vectors
2. **Embeddings → Classification**: Logistic regression model trained on embeddings to predict sentiment classes

**Training configurations:**
- **LR_100**: Logistic regression trained on 100 labeled samples
- **LR_1000**: Logistic regression trained on 1,000 labeled samples  
- **LR_ALL**: Logistic regression trained on the full training dataset

**Cost considerations:** Training and inference costs for logistic regression are negligible compared to embedding generation costs.

### Fine-tuned Transformer Approaches
Traditional encoder-only transformer models (BERT) fine-tuned on the sentiment classification task:
- **BERT-base**: Fine-tuned BERT-base-uncased model trained on the full training dataset
- **Training process**: 5 epochs, batch size 16, learning rate 2e-05 on 24,985 training samples
- **Training infrastructure**: NVIDIA GeForce RTX 4060 Laptop GPU (8GB VRAM)
- **Training time**: 8.33 minutes (500 seconds)

**Cost considerations:** 
- **Training cost**: Based on Azure T4 GPU rental ($0.56/hour): $0.078 one-time training cost
- **Inference cost**: $0.014 per 1K samples (single GPU), $0.028 per 1K samples (2 redundant GPUs for reliability)
- **Infrastructure**: Requires GPU compute infrastructure for both training and inference
- **Deployment**: Self-hosted model, full control over infrastructure and data privacy

## Key Findings and Conclusions

### 1. **Approach Comparison: LLMs vs Fine-tuned LLMs vs Embedding+ML vs Fine-tuned BERT**
- **Best Overall Performance**: LR_ALL (Embedding + LR trained on full dataset) achieved the highest accuracy (73.2%) at minimal cost
- **Best Fine-tuned Performance**: LLM_FT_MINI_ZEROSHOT achieved 80.0% accuracy, outperforming all other approaches
- **BERT Performance**: BERT_SENTIMENT achieved 74.5% accuracy, outperforming LR_ALL and all base LLM approaches
- **Fine-tuning Impact**: Fine-tuned models show significant improvement over base models (79-80% vs 67-69% accuracy for LLMs)
- **LLM Advantages**: Better performance with limited training data, more robust to different text patterns
- **Fine-tuned LLM Advantages**: Highest single-model accuracy, faster inference than few-shot approaches, no prompt engineering needed
- **Embedding+ML Advantages**: Superior cost-effectiveness, faster inference, perfect reliability (100% completion rate)
- **BERT Advantages**: Excellent accuracy-to-cost ratio, very fast inference, local deployment, data privacy, balanced class performance
- **Training Data Impact**: Embedding+ML approaches show dramatic improvement with more training data (60.9% → 67.1% → 73.2%)

### 2. **Cost-Effectiveness Revolution**
- **Embedding+ML approaches** are 50-21,000x more cost-effective than LLM approaches
- **BERT approach** provides excellent accuracy-to-cost ratio at $0.028 per 1K samples (5th most cost-effective)
- **LR_ALL** provides the best accuracy at $0.0005 per 1K samples vs $0.025-$10.67 for LLM approaches
- **Prompt caching impact**: Few-shot approaches benefit from 50% discount on cached input tokens, reducing actual costs by ~40%
- **Fine-tuned models** have 2x token costs compared to base models (OpenAI pricing) plus significant upfront training investment ($39.24 per model)
- **BERT training cost**: Minimal one-time cost of $0.078 for training, infrastructure flexibility
- **Break-even analysis**: 
  - Embedding+ML becomes cost-effective after ~1,000 predictions
  - BERT becomes cost-effective vs LLMs after ~100-1,000 predictions depending on approach
  - Fine-tuned LLMs break even vs few-shot approaches after ~500-19,000 predictions (depending on prompt complexity)
  - Cached pricing makes few-shot approaches more competitive but still higher than embedding+ML and BERT
  - Azure hosting costs would add ongoing expense but lower per-token costs for fine-tuned models

### 3. **Performance vs Training Data Size**
- **LR_100**: Insufficient training data leads to poor neutral class detection (38.3% accuracy)
- **LR_1000**: Significant improvement, reaching competitive performance with LLM zero-shot approaches
- **LR_ALL**: Exceeds all LLM approaches in overall accuracy and maintains balanced class performance

### 4. **Processing Speed and Scalability**
- **BERT approach** provides fastest processing (0.09s per sample) with fully local inference
- **Embedding+ML approaches** are 2-17x faster than LLM approaches (but include network latency)
- **Fine-tuned models** are 1.7-4.5x faster than corresponding base models with few-shot prompting
- **Perfect reliability**: 100% completion rate for embedding+ML and BERT vs 97-99% for LLMs due to outputs errors (model outputs not matching expected classes) or safety filters (model refusing to answer on certain inputs)
- **Scalability**: BERT and embedding+ML approaches can handle much higher throughput for production workloads
- **Network independence**: BERT offers consistent performance without dependency on cloud API availability

### 5. **Fine-tuning vs Few-shot Comparison**
- **Fine-tuned zero-shot** consistently outperforms base model few-shot approaches (79-80% vs 67-69%)
- **Training overhead**: One-time fine-tuning cost vs ongoing prompt complexity and token usage
- **Maintenance**: Fine-tuned models require retraining for dataset updates vs dynamic few-shot examples
- **Deployment**: Fine-tuned models need hosting infrastructure vs stateless API calls

### 6. **Class-Specific Performance Insights**
- **Neutral sentiment** remains challenging across all approaches but BERT achieves excellent neutral detection (73.5%), competitive with fine-tuned LLMs
- **Fine-tuned models** show strong performance across all classes, with fine-tuned mini achieving best neutral detection among LLM approaches (74.7%)
- **BERT** shows well-balanced performance across all sentiment classes (70.9% negative, 73.5% neutral, 78.6% positive)
- **Negative sentiment** detection is consistently strong across approaches (69-87% accuracy)
- **Positive sentiment** shows good performance across all methods (68-85% accuracy)

## Recommendations

### For Production Use Cases:

1. **Cost-Sensitive High-Volume Applications**: Use **LR_ALL (Embedding + LR on full dataset)**
   - Excellent accuracy (73.2%) at lowest cost per prediction ($0.0005 per 1K samples)
   - Good processing speed (5.58 samples/sec)
   - Perfect reliability (100% completion rate)
   - **Ideal for**: Cost-sensitive deployments, large-scale batch processing, applications where cost optimization is primary concern

2. **Highest Accuracy Requirements**: Use **LLM_FT_MINI_ZEROSHOT (Fine-tuned Mini)**
   - Highest single-model accuracy (80.0%)
   - Higher cost ($0.202 per 1K samples due to 2x token pricing)
   - Fast processing (3.30 samples/sec)
   - No prompt engineering required
   - **Ideal for**: Critical applications requiring maximum accuracy, where training investment and higher costs are justified

3. **Balanced Performance with Speed Priority**: Use **BERT_SENTIMENT**
   - Best accuracy (74.5%) with fastest processing (11.19 samples/sec)
   - Good cost-effectiveness ($0.028 per 1K samples)
   - Perfect reliability (100% completion rate)
   - Local deployment with data privacy
   - **Ideal for**: Real-time applications, performance-critical systems, regulatory compliance, hybrid cloud deployments

4. **LLM Approach with Cost Control**: Use **LLM_FT_NANO_ZEROSHOT (Fine-tuned Nano)**
   - Strong accuracy (79.0%) with controlled costs
   - Moderate cost increase over base nano ($0.050 vs $0.025 per 1K samples)
   - Good processing speed (2.71 samples/sec)
   - **Ideal for**: Applications needing LLM robustness with budget constraints

5. **Limited Training Data Scenarios**: Use **LR_1000**
   - Good accuracy (67.1%) competitive with base LLM zero-shot approaches
   - Extremely low cost ($0.0005 per 1K samples)
   - Fast processing (5.47 samples/sec)
   - **Ideal for**: Applications where collecting large training datasets is challenging

6. **Rapid Prototyping/Exploration**: Use **LLM_NANO_ZEROSHOT**
   - No training data required
   - Decent accuracy (67.7%)
   - Moderate cost ($0.025 per 1K samples)
   - **Ideal for**: Quick prototypes, one-off analyses, exploratory work, proof-of-concept development

### Deployment Strategy Recommendations:

**For New Projects:**
- **Start with LR_1000** if you have 1000+ labeled samples for cost-effective baseline
- **Scale to LR_ALL** as you collect more training data for maximum cost efficiency
- **Consider BERT** when you need higher accuracy than embedding+ML with fast processing and data privacy
- **Consider fine-tuned LLMs** when you need maximum accuracy and can justify training costs

**For Existing Systems:**
- **Migrate from base LLMs to BERT** for immediate accuracy and speed improvements with cost reduction
- **Use base LLM approaches** only when training data is unavailable or for handling edge cases
- **Implement hybrid approaches**: Use embedding+ML for bulk processing, BERT for performance-critical tasks, LLMs for edge cases

**Optimization Strategies:**
- **Few-shot with caching**: If using few-shot approaches, ensure consistent example ordering to maximize cache benefits
- **Infrastructure planning**: BERT requires GPU infrastructure but offers operational independence
- **Cost monitoring**: Track actual vs estimated costs, especially for cached LLM approaches

### Avoid:
- **LR_100**: Insufficient training data leads to poor performance
- **Few-shot with 1000 examples**: Poor cost-benefit ratio even with caching compared to training embedding+ML models or fine-tuning
- **Base LLM approaches for high-volume production** unless training data is completely unavailable

**Note on pricing**: Cached pricing estimates assume ~85% of few-shot input tokens are cached (50% discount). Actual caching depends on request patterns and cache retention.

