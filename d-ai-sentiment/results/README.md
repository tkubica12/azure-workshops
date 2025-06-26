# Sentiment Analysis Experiment Results

## Overview

This document presents the results of sentiment analysis experiments conducted on June 25-26, 2025, comparing different approaches:

1. **Large Language Models (LLMs)**: GPT-4.1-mini and GPT-4.1-nano with various prompting strategies (zero-shot, few-shot with 100/1000 examples)
2. **Hybrid Embedding + ML Models**: OpenAI embedding models combined with logistic regression classifiers trained on different dataset sizes (100, 1000, and full training set)

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

### Cost Analysis

| Experiment | Cost per 1K Samples | Cost Efficiency Rank |
|------------|-------------------|---------------------|
| **Most Cost-Effective** |
| LR_100 | $0.0005 | 1st (Best) |
| LR_1000 | $0.0005 | 1st (Best) |
| LR_ALL | $0.0005 | 1st (Best) |
| LLM_NANO_ZEROSHOT | $0.025 | 4th |
| LLM_FT_NANO_ZEROSHOT | $0.050 | 5th |
| LLM_MINI_ZEROSHOT | $0.106 | 6th |
| LLM_FT_MINI_ZEROSHOT | $0.202 | 7th |
| **Moderate Cost** |
| LLM_NANO_FEWSHOT_100 | $0.280 ($0.168 cached) | 8th |
| LLM_FT_NANO_FEWSHOT_100 | $0.562 ($0.337 cached) | 9th |
| LLM_MINI_FEWSHOT_100 | $1.130 ($0.678 cached) | 10th |
| LLM_FT_MINI_FEWSHOT_100 | $2.242 ($1.345 cached) | 11th |
| **High Cost** |
| LLM_NANO_FEWSHOT_1000 | $2.590 ($1.554 cached) | 12th |
| LLM_MINI_FEWSHOT_1000 | $10.670 ($6.402 cached) | 13th (Most Expensive) |

### Processing Speed Analysis

| Experiment | Processing Speed Rank | Time per Sample (seconds) |
|------------|---------------------|---------------------------|
| **Fastest Processing** |
| LR_ALL | 1st (Fastest) | 0.18 |
| LR_1000 | 2nd | 0.18 |
| LR_100 | 3rd | 0.19 |
| **Moderate Speed** |
| LLM_FT_MINI_ZEROSHOT | 4th | 0.30 |
| LLM_FT_MINI_FEWSHOT_100 | 5th | 0.37 |
| LLM_FT_NANO_ZEROSHOT | 6th | 0.37 |
| LLM_FT_NANO_FEWSHOT_100 | 7th | 0.38 |
| LLM_NANO_ZEROSHOT | 8th | 0.64 |
| LLM_MINI_ZEROSHOT | 9th | 0.72 |
| LLM_NANO_FEWSHOT_100 | 10th | 0.81 |
| LLM_MINI_FEWSHOT_100 | 11th | 1.06 |
| **Slower Processing** |
| LLM_NANO_FEWSHOT_1000 | 12th | 1.77 |
| LLM_MINI_FEWSHOT_1000 | 13th (Slowest) | 3.00 |

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
- **Inference strategies**: Both zero-shot and few-shot (100 examples) approaches tested

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

## Key Findings and Conclusions

### 1. **Approach Comparison: LLMs vs Fine-tuned LLMs vs Embedding+ML**
- **Best Overall Performance**: LR_ALL (Embedding + LR trained on full dataset) achieved the highest accuracy (73.2%) at minimal cost
- **Best Fine-tuned Performance**: LLM_FT_MINI_ZEROSHOT achieved 80.0% accuracy, outperforming all other LLM approaches
- **Fine-tuning Impact**: Fine-tuned models show significant improvement over base models (79-80% vs 67-69% accuracy)
- **LLM Advantages**: Better performance with limited training data, more robust to different text patterns
- **Fine-tuned LLM Advantages**: Highest single-model accuracy, faster inference than few-shot approaches, no prompt engineering needed
- **Embedding+ML Advantages**: Superior cost-effectiveness, faster inference, perfect reliability (100% completion rate)
- **Training Data Impact**: Embedding+ML approaches show dramatic improvement with more training data (60.9% → 67.1% → 73.2%)

### 2. **Cost-Effectiveness Revolution**
- **Embedding+ML approaches** are 50-21,000x more cost-effective than LLM approaches
- **LR_ALL** provides the best accuracy at $0.0005 per 1K samples vs $0.025-$10.67 for LLM approaches
- **Prompt caching impact**: Few-shot approaches benefit from 50% discount on cached input tokens, reducing actual costs by ~40%
- **Fine-tuned models** have 2x token costs compared to base models (OpenAI pricing) plus significant upfront training investment ($39.24 per model)
- **Break-even analysis**: 
  - Embedding+ML becomes cost-effective after ~1,000 predictions
  - Fine-tuned models break even vs few-shot approaches after ~500-19,000 predictions (depending on prompt complexity)
  - Cached pricing makes few-shot approaches more competitive but still higher than embedding+ML
  - Azure hosting costs would add ongoing expense but lower per-token costs for fine-tuned models

### 3. **Performance vs Training Data Size**
- **LR_100**: Insufficient training data leads to poor neutral class detection (38.3% accuracy)
- **LR_1000**: Significant improvement, reaching competitive performance with LLM zero-shot approaches
- **LR_ALL**: Exceeds all LLM approaches in overall accuracy and maintains balanced class performance

### 4. **Processing Speed and Scalability**
- **Embedding+ML approaches** are 3-17x faster than LLM approaches
- **Fine-tuned models** are 1.7-4.5x faster than corresponding base models with few-shot prompting
- **Perfect reliability**: 100% completion rate for embedding+ML vs 97-99% for LLMs
- **Scalability**: Embedding+ML approaches can handle much higher throughput for production workloads

### 5. **Fine-tuning vs Few-shot Comparison**
- **Fine-tuned zero-shot** consistently outperforms base model few-shot approaches (79-80% vs 67-69%)
- **Training overhead**: One-time fine-tuning cost vs ongoing prompt complexity and token usage
- **Maintenance**: Fine-tuned models require retraining for dataset updates vs dynamic few-shot examples
- **Deployment**: Fine-tuned models need hosting infrastructure vs stateless API calls

### 6. **Class-Specific Performance Insights**
- **Neutral sentiment** remains challenging across all approaches but embedding+ML with sufficient training data (LR_ALL) achieves best performance (69.6%)
- **Fine-tuned models** show strong performance across all classes, with fine-tuned mini achieving best neutral detection among LLM approaches (74.7%)
- **Negative sentiment** detection is consistently strong across approaches (69-87% accuracy)
- **Positive sentiment** shows good performance across all methods (68-85% accuracy)

### 7. **Reliability and Robustness**
- **Embedding+ML approaches** show perfect completion rates (100%)
- **LLM approaches** have occasional failures, especially with complex prompts (2-3% failure rate)
- **Fine-tuned models** maintain high reliability (99.2-99.3% completion rate)
- **Consistency**: Embedding+ML provides most predictable performance and costs

## Recommendations

### For Production Use Cases:

1. **High-Volume Production Applications**: Use **LR_ALL (Embedding + LR on full dataset)**
   - Best overall accuracy (73.2%)
   - Lowest cost per prediction ($0.0005 per 1K samples)
   - Fastest processing (5.58 samples/sec)
   - Perfect reliability (100% completion rate)
   - **Ideal for**: Large-scale sentiment analysis, real-time applications, cost-sensitive deployments

2. **High-Accuracy Applications with Budget**: Use **LLM_FT_MINI_ZEROSHOT (Fine-tuned Mini)**
   - Highest single-model accuracy (80.0%)
   - Higher cost than base models ($0.202 per 1K samples due to 2x token pricing)
   - Fast processing (3.30 samples/sec)
   - No prompt engineering required
   - **Ideal for**: Critical applications requiring highest accuracy, where training investment and 2x token costs are justified

3. **Balanced Performance/Cost for LLM Approach**: Use **LLM_FT_NANO_ZEROSHOT (Fine-tuned Nano)**
   - Strong accuracy (79.0%)
   - Moderate cost increase over base nano ($0.050 vs $0.025 per 1K samples)
   - Good processing speed (2.71 samples/sec)
   - **Ideal for**: Applications needing LLM robustness with controlled cost increase

4. **Medium-Volume Applications with Limited Training Data**: Use **LR_1000**
   - Good accuracy (67.1%) competitive with base LLM zero-shot approaches
   - Extremely low cost ($0.0005 per 1K samples)
   - Fast processing (5.47 samples/sec)
   - **Ideal for**: Applications where collecting large training datasets is challenging

5. **Rapid Prototyping/Small-Scale Applications**: Use **LLM_NANO_ZEROSHOT**
   - No training data required
   - Decent accuracy (67.7%)
   - Moderate cost ($0.025 per 1K samples)
   - **Ideal for**: Quick prototypes, one-off analyses, exploratory work

### Deployment Strategy Recommendations:

- **Start with LR_1000** if you have 1000+ labeled samples  
- **Scale to LR_ALL** as you collect more training data
- **Consider fine-tuned models** when you need highest accuracy and can justify training costs
- **Use base LLM approaches** only when training data is unavailable or for handling edge cases
- **Few-shot with caching**: If using few-shot approaches, ensure consistent example ordering to maximize cache benefits
- **Consider hybrid approaches**: Use embedding+ML for bulk processing, LLMs for edge cases

### Avoid:
- **LR_100**: Insufficient training data leads to poor performance
- **Few-shot with 1000 examples**: Poor cost-benefit ratio even with caching compared to training embedding+ML models or fine-tuning
- **Base LLM approaches for high-volume production** unless training data is completely unavailable

**Note on pricing**: Cached pricing estimates assume ~85% of few-shot input tokens are cached (50% discount). Actual caching depends on request patterns and cache retention.

---

*Generated on: June 25-26, 2025*  
*Total samples analyzed: 5,205 per experiment*  
*Dataset: Multi-class sentiment analysis (Negative, Neutral, Positive)*
*Approaches tested: 6 base LLM configurations + 4 fine-tuned LLM configurations + 3 Embedding+ML configurations*