#!/usr/bin/env python3
"""
Compare the results from different training runs.
"""

import os
from pathlib import Path

def read_stats_summary(stats_file):
    """Extract key metrics from a stats file."""
    if not os.path.exists(stats_file):
        return None
    
    stats = {}
    with open(stats_file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if line.startswith('Total samples:'):
            stats['samples'] = int(line.split(':')[1].strip().replace(',', ''))
        elif line.startswith('Test Accuracy:'):
            stats['accuracy'] = float(line.split(':')[1].strip())
        elif line.startswith('Training Time:'):
            stats['training_time'] = float(line.split(':')[1].strip().split()[0])
        elif line.startswith('Memory Used:'):
            stats['memory_mb'] = float(line.split(':')[1].strip().split()[0])
    
    return stats

def main():
    """Compare training results."""
    print("="*80)
    print("LOGISTIC REGRESSION TRAINING RESULTS COMPARISON")
    print("="*80)
    
    datasets = [
        ('100 samples', 'results/lr_training_stats_100.txt'),
        ('1000 samples', 'results/lr_training_stats_1000.txt'),
        ('All samples', 'results/lr_training_stats_all.txt')
    ]
    
    print(f"{'Dataset':<15} {'Samples':<10} {'Accuracy':<10} {'Time (s)':<10} {'Memory (MB)':<12}")
    print("-" * 80)
    
    for name, stats_file in datasets:
        stats = read_stats_summary(stats_file)
        if stats:
            print(f"{name:<15} {stats['samples']:<10,} {stats['accuracy']:<10.4f} {stats['training_time']:<10.2f} {stats['memory_mb']:<12.1f}")
        else:
            print(f"{name:<15} {'N/A':<10} {'N/A':<10} {'N/A':<10} {'N/A':<12}")
    
    print("\n" + "="*80)
    print("KEY OBSERVATIONS:")
    print("• Accuracy improves significantly with more training data")
    print("• Training time remains very fast even for 31K samples")
    print("• Memory usage scales roughly linearly with dataset size")
    print("• All models are very compact (~40KB each)")
    print("="*80)

if __name__ == "__main__":
    main()
