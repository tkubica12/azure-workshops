"""
Analysis utilities for sentiment analysis experiments.
Provides centralized functionality for running experiments, saving results, and generating reports.
"""

import os
import pandas as pd
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from collections import Counter
import time

logger = logging.getLogger(__name__)

input_token_cost_per_1k = 0.0001
output_token_cost_per_1k = 0.0004 


class AnalysisUtils:
    """Utility class for sentiment analysis experiments."""
    
    def __init__(self, experiment_name: str = "experiment"):
        """
        Initialize analysis utilities.
          Args:
            experiment_name: Name of the experiment for file naming
        """
        self.experiment_name = experiment_name
        self.testing_mode = os.getenv("TESTING_MODE", "true").lower() == "true"
        self.testing_samples = int(os.getenv("TESTING_SAMPLES", "1")) if self.testing_mode else None
    
    def load_validation_data(self, data_path: str = "dataset/val_df.csv") -> pd.DataFrame:
        """
        Load the validation dataset.
        
        Args:
            data_path: Path to validation dataset
            
        Returns:
            DataFrame with validation data
        """
        val_path = Path(data_path)
        if not val_path.exists():
            raise FileNotFoundError(f"Validation dataset not found at {val_path}")
        
        df = pd.read_csv(val_path)
        logger.info(f"Loaded validation dataset with {len(df)} samples")
        return df
    
    def load_existing_results(self, results_file: Path) -> pd.DataFrame:
        """
        Load existing results if the file exists.
        
        Args:
            results_file: Path to results file
            
        Returns:
            DataFrame with existing results or empty DataFrame
        """
        if results_file.exists():
            df = pd.read_csv(results_file)
            logger.info(f"Found existing results file with {len(df)} processed samples")
            return df
        else:
            logger.info("No existing results file found, starting from scratch")
            return pd.DataFrame()
    
    def save_results(self, df: pd.DataFrame, results_file: Path):
        """
        Save results to CSV file.
        
        Args:
            df: DataFrame with results
            results_file: Path to save results
        """
        df.to_csv(results_file, index=False)
        logger.info(f"Results saved to {results_file}")
    
    def setup_results_file(self) -> Path:
        """
        Setup results file with timestamp.
        
        Returns:
            Path to results file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = Path(f"results/{self.experiment_name}_results_{timestamp}.csv")
        results_file.parent.mkdir(exist_ok=True)
        return results_file
    
    def generate_report(self, df: pd.DataFrame) -> str:
        """
        Generate a summary report of the classification results.
        
        Args:
            df: DataFrame with results        Returns:
            Formatted report string
        """
        total_samples = len(df)
        completed_predictions = len(df[df['predicted_label'].notna()])
        failed_predictions = total_samples - completed_predictions
        
        if completed_predictions == 0:
            return "No completed predictions to evaluate."
        
        # Calculate accuracy only for completed predictions
        completed_df = df[df['predicted_label'].notna()].copy()
        completed_df['correct'] = completed_df['label'] == completed_df['predicted_label']
        accuracy = completed_df['correct'].mean()
        correct_predictions = len(completed_df[completed_df['correct']])
        incorrect_predictions = completed_predictions - correct_predictions
        
        # Confusion matrix for completed predictions
        actual_counts = Counter(completed_df['label'])
        predicted_counts = Counter(completed_df['predicted_label'])
        correct_counts = Counter(completed_df[completed_df['correct']]['label'])
        
        report = f"""
=== SENTIMENT ANALYSIS RESULTS ===
Experiment: {self.experiment_name.upper()}
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERALL STATISTICS:
- Total samples: {total_samples}
- Completed predictions: {completed_predictions} ({completed_predictions/total_samples*100:.1f}%)
- Failed predictions: {failed_predictions} ({failed_predictions/total_samples*100:.1f}%)
- Correct predictions: {correct_predictions} ({correct_predictions/total_samples*100:.1f}%)
- Incorrect predictions: {incorrect_predictions} ({incorrect_predictions/total_samples*100:.1f}%)
- Overall accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)

LABEL DISTRIBUTION (ACTUAL):
- Negative (0): {actual_counts.get(0, 0)} samples
- Neutral (1): {actual_counts.get(1, 0)} samples  
- Positive (2): {actual_counts.get(2, 0)} samples

LABEL DISTRIBUTION (PREDICTED):
- Negative (0): {predicted_counts.get(0, 0)} samples
- Neutral (1): {predicted_counts.get(1, 0)} samples
- Positive (2): {predicted_counts.get(2, 0)} samples

ACCURACY BY CLASS:
- Negative (0): {correct_counts.get(0, 0)}/{actual_counts.get(0, 0)} = {correct_counts.get(0, 0)/max(actual_counts.get(0, 1), 1):.3f}
- Neutral (1): {correct_counts.get(1, 0)}/{actual_counts.get(1, 0)} = {correct_counts.get(1, 0)/max(actual_counts.get(1, 1), 1):.3f}
- Positive (2): {correct_counts.get(2, 0)}/{actual_counts.get(2, 0)} = {correct_counts.get(2, 0)/max(actual_counts.get(2, 1), 1):.3f}
"""
        return report
    
    def save_report(self, report: str, results_file: Path):
        """
        Save report to file.        
        Args:
            report: Report string
            results_file: Base results file path (will change extension to .txt)
        """
        report_file = results_file.with_suffix('.txt')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"Report saved to {report_file}")
    
    def run_experiment(
        self, 
        classifier_func: Callable[[str], Optional[int]], 
        data_path: str = "dataset/val_df.csv",
        resume: bool = True,
        llm_utils=None,
        display_progress: bool = True,
        display_interval: int = 25,
        model_config: dict = None    ) -> tuple[pd.DataFrame, str]:
        """
        Run a sentiment analysis experiment with optional progress tracking.
        
        Args:
            classifier_func: Function that takes text and returns predicted label (0, 1, 2) or None
            data_path: Path to validation dataset
            resume: Whether to resume from existing results
            llm_utils: LLM utility instance for token tracking (optional)
            display_progress: Whether to display progress updates
            display_interval: How often to display progress (every N samples)
            model_config: Model configuration dictionary with deployment_name and pricing (optional)
            
        Returns:
            Tuple of (results_dataframe, report_string)
        """
        experiment_start_time = time.time()
        
        # Load validation data
        val_df = self.load_validation_data(data_path)
        total_samples = len(val_df)
          # Display experiment start if requested
        if display_progress:
            self.display_experiment_start(
                data_path=data_path,
                model_config=model_config,
                total_samples=total_samples,
                display_interval=display_interval
            )
        
        # Setup progress tracking if requested
        if display_progress:
            progress_wrapper, progress_state = self.create_progress_tracker(
                llm_utils=llm_utils,
                total_samples=total_samples,
                display_interval=display_interval
            )
            classifier_func = progress_wrapper(classifier_func)
        
        # Setup results file
        results_file = self.setup_results_file()
        
        # Load existing results if resuming
        existing_results = pd.DataFrame()
        processed_ids = set()
        start_idx = 0
        
        if resume:
            existing_results = self.load_existing_results(results_file)
            if len(existing_results) > 0:
                processed_ids = set(existing_results['id'])
                start_idx = len(existing_results)
                logger.info(f"Resuming from index {start_idx}")
        
        # Prepare results dataframe
        if len(existing_results) > 0:
            results_df = existing_results.copy()
        else:
            results_df = pd.DataFrame(columns=['id', 'text', 'label', 'sentiment', 'predicted_label', 'correct'])
          # Process samples
        processed_count = 0
        for idx, row in val_df.iterrows():
            if idx < start_idx or row['id'] in processed_ids:
                continue
                
            logger.info(f"Processing sample {idx + 1}/{len(val_df)}: ID {row['id']}")
            
            # Classify sentiment
            predicted_label = classifier_func(row['text'])
            
            # Prepare result row
            result_row = {
                'id': row['id'],
                'text': row['text'],
                'label': row['label'],
                'sentiment': row['sentiment'],
                'predicted_label': predicted_label,
                'correct': predicted_label == row['label'] if predicted_label is not None else None
            }
            
            # Add to results
            results_df = pd.concat([results_df, pd.DataFrame([result_row])], ignore_index=True)
            
            # Save results incrementally
            self.save_results(results_df, results_file)
            
            logger.info(f"Sample {row['id']}: Actual={row['label']}, Predicted={predicted_label}, "
                       f"Correct={result_row['correct']}")
            
            processed_count += 1
              # Break after specified number of samples in testing mode
            if self.testing_mode and processed_count >= self.testing_samples:
                logger.info(f"Testing mode: Breaking after {processed_count} samples")
                break
        
        # Generate and save report
        report = self.generate_report(results_df)
        
        # Add completion section to the report
        completion_section = self.generate_completion_section(
            start_time=experiment_start_time,
            llm_utils=llm_utils,
            model_config=model_config
        )
        full_report = completion_section + report
        
        self.save_report(full_report, results_file)
        
        # Display final results if progress tracking was enabled
        if display_progress:
            self.display_final_results(
                start_time=experiment_start_time,
                llm_utils=llm_utils,
                model_config=model_config,
                report=report
            )
        
        return results_df, report
    
    def create_progress_tracker(self, llm_utils=None, total_samples=None, display_interval=25):
        """
        Create a progress tracking wrapper for classification functions.
        
        Args:
            llm_utils: LLM utility instance with token tracking (optional)
            total_samples: Total number of samples to process (optional)
            display_interval: How often to display progress (every N samples)
            
        Returns:
            Tuple of (wrapper_function, progress_state_dict)
        """
        progress_state = {
            'processed_count': 0,
            'start_time': time.time(),
            'llm_utils': llm_utils
        }
        
        def progress_wrapper(classifier_func):
            def wrapped_classifier(text):
                progress_state['processed_count'] += 1
                
                # Call the actual classifier
                result = classifier_func(text)
                
                # Display progress at intervals
                if (progress_state['processed_count'] % display_interval == 0 or 
                    (total_samples and progress_state['processed_count'] == total_samples)):
                    self._display_progress(progress_state, total_samples, display_interval)
                
                return result
            
            return wrapped_classifier
        
        return progress_wrapper, progress_state

    def _display_progress(self, progress_state, total_samples=None, display_interval=25):
        """
        Display progress information including token usage if available.
        
        Args:
            progress_state: Dictionary containing progress tracking state
            total_samples: Total number of samples (optional)
            display_interval: Display interval for context
        """
        processed_count = progress_state['processed_count']
        start_time = progress_state['start_time']
        llm_utils = progress_state.get('llm_utils')
        elapsed_time = time.time() - start_time
        
        # Calculate rates
        samples_per_second = processed_count / elapsed_time if elapsed_time > 0 else 0
        
        progress_msg = f"\n{'='*80}\n"
        progress_msg += f"PROGRESS UPDATE - Sample {processed_count}"
        if total_samples:
            progress_msg += f" of {total_samples} ({processed_count/total_samples*100:.1f}%)"
        progress_msg += f"\n{'='*80}\n"
        
        # Add token usage if LLM utils available
        if llm_utils and hasattr(llm_utils, 'get_token_usage'):
            usage = llm_utils.get_token_usage()
            tokens_per_second = usage['total_tokens'] / elapsed_time if elapsed_time > 0 else 0
            
            progress_msg += f"📊 TOKEN USAGE (Cumulative):\n"
            progress_msg += f"   Input tokens:  {usage['total_input_tokens']:,}\n"
            progress_msg += f"   Output tokens: {usage['total_output_tokens']:,}\n"
            progress_msg += f"   Total tokens:  {usage['total_tokens']:,}\n"
            progress_msg += f"   API requests:  {usage['total_requests']:,}\n\n"
            
            progress_msg += f"⏱️  PERFORMANCE:\n"
            progress_msg += f"   Elapsed time:     {elapsed_time:.1f}s\n"
            progress_msg += f"   Samples/second:   {samples_per_second:.2f}\n"
            progress_msg += f"   Tokens/second:    {tokens_per_second:.1f}\n"
            progress_msg += f"   Avg tokens/sample: {usage['total_tokens']/processed_count:.1f}\n"
            
            # Estimate remaining time if total_samples is known
            if total_samples and processed_count < total_samples:
                remaining_samples = total_samples - processed_count
                eta_seconds = remaining_samples / samples_per_second if samples_per_second > 0 else 0
                progress_msg += f"   Estimated remaining: {eta_seconds:.0f}s\n"
        else:
            progress_msg += f"⏱️  PROGRESS:\n"
            progress_msg += f"   Elapsed time:     {elapsed_time:.1f}s\n"
            progress_msg += f"   Samples/second:   {samples_per_second:.2f}\n"
            
            if total_samples and processed_count < total_samples:
                remaining_samples = total_samples - processed_count
                eta_seconds = remaining_samples / samples_per_second if samples_per_second > 0 else 0
                progress_msg += f"   Estimated remaining: {eta_seconds:.0f}s\n"        
        progress_msg += f"{'='*80}"
        
        print(progress_msg)
        logger.info(f"Progress: {processed_count} samples processed")

    def display_experiment_start(self, data_path, model_config=None, total_samples=None, display_interval=25):
        """
        Display experiment start information.
        
        Args:
            data_path: Path to data file
            model_config: Model configuration dictionary (optional)
            total_samples: Total samples to process (optional)
            display_interval: Progress update interval
        """
        print(f"\n{'='*80}")
        print(f"🚀 STARTING {self.experiment_name.upper()} EXPERIMENT")
        print(f"{'='*80}")
        print(f"📁 Data file: {data_path}")
        if model_config:
            print(f"🤖 Model: {model_config.get('model_display_name', model_config.get('deployment_name', 'Unknown'))}")
            print(f"💰 Pricing: ${model_config.get('input_cost_per_1k', 0):.5f}/1K input, ${model_config.get('output_cost_per_1k', 0):.5f}/1K output tokens")
        print(f"📊 Progress updates every {display_interval} samples")
        if total_samples:
            print(f"🎯 Total samples: {total_samples}")
        print(f"{'='*80}\n")

    def display_final_results(self, start_time, llm_utils=None, model_config=None, report=None):
        """
        Display final experiment results including token usage and performance metrics.
        
        Args:
            start_time: Experiment start time
            llm_utils: LLM utility instance with token tracking (optional)
            model_config: Model configuration dictionary with pricing (optional)
            report: Classification report to display (optional)
        """
        total_time = time.time() - start_time
        
        print(f"\n{'='*80}")
        print("🎉 EXPERIMENT COMPLETED!")
        print(f"{'='*80}")
        if model_config:
            print(f"🤖 Model: {model_config.get('model_display_name', model_config.get('deployment_name', 'Unknown'))}")
        print(f"⏱️  Total execution time: {total_time:.1f} seconds")
        
        # Display token usage if available
        if llm_utils and hasattr(llm_utils, 'get_token_usage'):
            final_usage = llm_utils.get_token_usage()
            
            print(f"\n📊 FINAL TOKEN USAGE:")
            print(f"   Total input tokens:  {final_usage['total_input_tokens']:,}")
            print(f"   Total output tokens: {final_usage['total_output_tokens']:,}")
            print(f"   Total tokens:        {final_usage['total_tokens']:,}")
            print(f"   Total API requests:  {final_usage['total_requests']:,}")
            
            print(f"\n📈 FINAL PERFORMANCE METRICS:")
            processed_samples = final_usage['total_requests']
            if processed_samples > 0 and total_time > 0:
                print(f"   Samples processed:   {processed_samples:,}")
                print(f"   Samples per second:  {processed_samples/total_time:.2f}")
                print(f"   Tokens per second:   {final_usage['total_tokens']/total_time:.1f}")
                print(f"   Avg tokens/sample:   {final_usage['total_tokens']/processed_samples:.1f}")
            
            # Cost estimation using model-specific pricing
            if final_usage['total_tokens'] > 0:
                if model_config:
                    input_cost_per_1k = model_config.get('input_cost_per_1k', 0.00015)
                    output_cost_per_1k = model_config.get('output_cost_per_1k', 0.0006)
                    print(f"   Input cost rate:     ${input_cost_per_1k:.5f} per 1K tokens")
                    print(f"   Output cost rate:    ${output_cost_per_1k:.5f} per 1K tokens")
                else:
                    # Fallback to default pricing
                    input_cost_per_1k = 0.00015
                    output_cost_per_1k = 0.0006
                    print(f"   Using default pricing rates")
                
                estimated_cost = (
                    (final_usage['total_input_tokens'] / 1000) * input_cost_per_1k +
                    (final_usage['total_output_tokens'] / 1000) * output_cost_per_1k
                )
                print(f"   Estimated cost:      ${estimated_cost:.4f}")
        
        print(f"{'='*80}\n")
          # Display classification report
        if report:
            print("📋 CLASSIFICATION REPORT:")
            print("="*80)
            print(report)
    
    def generate_completion_section(self, start_time, llm_utils=None, model_config=None):
        """
        Generate the experiment completion section as a string.
        
        Args:
            start_time: Experiment start time
            llm_utils: LLM utility instance with token tracking (optional)
            model_config: Model configuration dictionary with pricing (optional)
              Returns:
            String containing the completion section
        """
        total_time = time.time() - start_time
        
        completion_section = f"{'='*80}\n"
        completion_section += "🎉 EXPERIMENT COMPLETED!\n"
        completion_section += f"{'='*80}\n"
        if model_config:
            completion_section += f"🤖 Model: {model_config.get('model_display_name', model_config.get('deployment_name', 'Unknown'))}\n"
        completion_section += f"⏱️  Total execution time: {total_time:.1f} seconds\n"
        
        # Add token usage if available
        if llm_utils and hasattr(llm_utils, 'get_token_usage'):
            final_usage = llm_utils.get_token_usage()
            
            completion_section += f"\n📊 FINAL TOKEN USAGE:\n"
            completion_section += f"   Total input tokens:  {final_usage['total_input_tokens']:,}\n"
            completion_section += f"   Total output tokens: {final_usage['total_output_tokens']:,}\n"
            completion_section += f"   Total tokens:        {final_usage['total_tokens']:,}\n"
            completion_section += f"   Total API requests:  {final_usage['total_requests']:,}\n"
            
            completion_section += f"\n📈 FINAL PERFORMANCE METRICS:\n"
            processed_samples = final_usage['total_requests']
            if processed_samples > 0 and total_time > 0:
                completion_section += f"   Samples processed:   {processed_samples:,}\n"
                completion_section += f"   Samples per second:  {processed_samples/total_time:.2f}\n"
                completion_section += f"   Tokens per second:   {final_usage['total_tokens']/total_time:.1f}\n"
                completion_section += f"   Avg tokens/sample:   {final_usage['total_tokens']/processed_samples:.1f}\n"
              # Cost estimation using model-specific pricing
            if final_usage['total_tokens'] > 0:
                if model_config:
                    input_cost_per_1k = model_config.get('input_cost_per_1k', 0.00015)
                    output_cost_per_1k = model_config.get('output_cost_per_1k', 0.0006)
                    completion_section += f"   Input cost rate:     ${input_cost_per_1k:.5f} per 1K tokens\n"
                    completion_section += f"   Output cost rate:    ${output_cost_per_1k:.5f} per 1K tokens\n"
                else:
                    # Fallback to default pricing
                    input_cost_per_1k = 0.00015
                    output_cost_per_1k = 0.0006
                    completion_section += f"   Using default pricing rates\n"
                
                estimated_cost = (
                    (final_usage['total_input_tokens'] / 1000) * input_cost_per_1k +
                    (final_usage['total_output_tokens'] / 1000) * output_cost_per_1k
                )
                completion_section += f"   Estimated cost:      ${estimated_cost:.4f}\n"
        
        completion_section += f"{'='*80}\n\n"
        completion_section += "📋 CLASSIFICATION REPORT:\n"
        completion_section += "="*80 + "\n\n"
        
        return completion_section
