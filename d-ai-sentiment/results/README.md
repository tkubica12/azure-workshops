# Sentiment Analysis Experiment Results

## Overview

This document presents the results of sentiment analysis experiments conducted on June 25, 2025, comparing different models (GPT-4.1-mini and GPT-4.1-nano) and prompting strategies (zero-shot, few-shot with 100 examples, and few-shot with 1000 examples).

## Experiment Comparison Table

| Experiment | Model | Strategy | Accuracy | Completed Predictions | Failed Predictions | Total Tokens | Input Tokens | Output Tokens | Estimated Cost | Execution Time | Samples/sec |
|------------|-------|----------|----------|---------------------|-------------------|--------------|--------------|---------------|----------------|----------------|-------------|
| LLM_NANO_ZEROSHOT | GPT-4.1-nano | Zero-shot | 67.7% | 5,166 (99.3%) | 39 (0.7%) | 1,289,946 | 1,284,780 | 5,166 | $0.13 | 3,306.7s | 1.56 |
| LLM_NANO_FEWSHOT_100 | GPT-4.1-nano | Few-shot (100) | 68.6% | 5,165 (99.2%) | 40 (0.8%) | 14,470,776 | 14,465,611 | 5,165 | $1.45 | 4,215.4s | 1.23 |
| LLM_NANO_FEWSHOT_1000 | GPT-4.1-nano | Few-shot (1000) | 68.4% | 5,166 (99.3%) | 39 (0.7%) | 133,890,834 | 133,885,668 | 5,166 | $13.39 | 9,160.4s | 0.56 |
| LLM_MINI_ZEROSHOT | GPT-4.1-mini | Zero-shot | 69.3% | 5,076 (97.5%) | 129 (2.5%) | 1,351,565 | 1,346,144 | 5,421 | $0.55 | 3,919.9s | 1.38 |
| LLM_MINI_FEWSHOT_100 | GPT-4.1-mini | Few-shot (100) | 69.4% | 5,140 (98.8%) | 65 (1.2%) | 14,688,863 | 14,683,620 | 5,243 | $5.88 | 5,565.6s | 0.94 |
| LLM_MINI_FEWSHOT_1000 | GPT-4.1-mini | Few-shot (1000) | 68.4% | 5,088 (97.8%) | 117 (2.2%) | 138,814,519 | 138,809,163 | 5,356 | $55.53 | 16,084.1s | 0.33 |

## Detailed Performance Metrics

### Accuracy by Sentiment Class

| Experiment | Negative Accuracy | Neutral Accuracy | Positive Accuracy |
|------------|------------------|------------------|-------------------|
| LLM_NANO_ZEROSHOT | 64.7% | 61.1% | 77.3% |
| LLM_NANO_FEWSHOT_100 | 62.9% | 73.0% | 68.6% |
| LLM_NANO_FEWSHOT_1000 | 74.2% | 57.9% | 74.7% |
| LLM_MINI_ZEROSHOT | 77.8% | 57.4% | 74.9% |
| LLM_MINI_FEWSHOT_100 | 74.6% | 60.3% | 74.9% |
| LLM_MINI_FEWSHOT_1000 | 71.7% | 59.9% | 74.8% |

### Cost Analysis

| Experiment | Cost per 1K Samples | Cost Efficiency Rank |
|------------|-------------------|---------------------|
| LLM_NANO_ZEROSHOT | $0.025 | 1st (Best) |
| LLM_NANO_FEWSHOT_100 | $0.280 | 3rd |
| LLM_NANO_FEWSHOT_1000 | $2.590 | 5th |
| LLM_MINI_ZEROSHOT | $0.106 | 2nd |
| LLM_MINI_FEWSHOT_100 | $1.130 | 4th |
| LLM_MINI_FEWSHOT_1000 | $10.670 | 6th (Most Expensive) |

### Processing Speed Analysis

| Experiment | Processing Speed Rank | Time per Sample (seconds) |
|------------|---------------------|---------------------------|
| LLM_NANO_ZEROSHOT | 1st (Fastest) | 0.64 |
| LLM_MINI_ZEROSHOT | 2nd | 0.72 |
| LLM_NANO_FEWSHOT_100 | 3rd | 0.81 |
| LLM_MINI_FEWSHOT_100 | 4th | 1.06 |
| LLM_NANO_FEWSHOT_1000 | 5th | 1.77 |
| LLM_MINI_FEWSHOT_1000 | 6th (Slowest) | 3.00 |

## Key Findings and Conclusions

### 1. **Accuracy vs Cost Trade-offs**
- **Best Overall Performance**: LLM_MINI_FEWSHOT_100 achieved the highest accuracy (69.4%) with reasonable cost ($5.88)
- **Most Cost-Effective**: LLM_NANO_ZEROSHOT provides decent accuracy (67.7%) at the lowest cost ($0.13)
- **Diminishing Returns**: Few-shot with 1000 examples doesn't significantly improve accuracy over 100 examples but dramatically increases costs

### 2. **Model Comparison**
- **GPT-4.1-mini** generally outperforms GPT-4.1-nano in accuracy but at 4-5x higher cost
- **GPT-4.1-nano** offers better cost efficiency and faster processing
- Both models show similar reliability (completion rates ~97-99%)

### 3. **Prompting Strategy Insights**
- **Zero-shot** approaches are most cost-effective and fastest
- **Few-shot with 100 examples** provides the best accuracy improvement per dollar spent
- **Few-shot with 1000 examples** shows marginal gains but exponential cost increases

### 4. **Class-Specific Performance**
- **Positive sentiment** is generally well-detected across all approaches (68-77% accuracy)
- **Negative sentiment** detection varies significantly between approaches (63-78% accuracy)
- **Neutral sentiment** is the most challenging, with accuracy ranging from 57-73%

### 5. **Reliability and Robustness**
- GPT-4.1-nano shows more consistent completion rates (99.2-99.3%)
- GPT-4.1-mini has slightly higher failure rates, especially with complex few-shot prompts

## Recommendations

### For Production Use Cases:

1. **High-Volume, Cost-Sensitive Applications**: Use **LLM_NANO_ZEROSHOT**
   - Lowest cost per prediction ($0.025 per 1K samples)
   - Fastest processing (1.56 samples/sec)
   - Acceptable accuracy (67.7%)

2. **Balanced Performance Requirements**: Use **LLM_MINI_FEWSHOT_100**
   - Best accuracy (69.4%)
   - Reasonable cost ($1.13 per 1K samples)
   - Good reliability (98.8% completion rate)

3. **High-Accuracy Critical Applications**: Consider **LLM_MINI_ZEROSHOT**
   - Second-best accuracy (69.3%)
   - Much lower cost than few-shot alternatives ($0.106 per 1K samples)
   - Good processing speed (1.38 samples/sec)

### Avoid:
- **Few-shot with 1000 examples** approaches due to poor cost-benefit ratio
- Consider the specific accuracy requirements for each sentiment class when choosing the approach

---

*Generated on: June 25, 2025*  
*Total samples analyzed: 5,205 per experiment*  
*Dataset: Multi-class sentiment analysis (Negative, Neutral, Positive)*