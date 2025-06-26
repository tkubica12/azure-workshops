"""
BERT utilities for sentiment analysis training and inference.
Provides centralized functionality for BERT-based sentiment classification.
"""
import os
import time
import logging
import torch
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, Optional, Any
from datetime import datetime
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    TrainingArguments, 
    Trainer,
    DataCollatorWithPadding,
    EarlyStoppingCallback
)
from datasets import Dataset
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import psutil

logger = logging.getLogger(__name__)


class BertUtils:
    """Utility class for BERT-based sentiment analysis training and inference."""
    
    def __init__(self, 
                 model_name: str = "bert-base-uncased",
                 num_labels: int = 3,
                 max_length: int = 128,
                 random_state: int = 42):
        """
        Initialize BertUtils.
        
        Args:
            model_name: Pre-trained model name from HuggingFace
            num_labels: Number of sentiment classes (0=negative, 1=neutral, 2=positive)
            max_length: Maximum sequence length for tokenization
            random_state: Random seed for reproducibility
        """
        self.model_name = model_name
        self.num_labels = num_labels
        self.max_length = max_length
        self.random_state = random_state
        
        # Initialize tokenizer
        self.tokenizer = None
        self.model = None
        
        # Device setup
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        if torch.cuda.is_available():
            logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
            logger.info(f"CUDA version: {torch.version.cuda}")
    
    def _get_device_info(self) -> Dict[str, Any]:
        """Get device and resource information."""
        info = {
            "device": str(self.device),
            "cpu_count": os.cpu_count(),
            "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2)
        }
        
        if torch.cuda.is_available():
            info.update({
                "gpu_name": torch.cuda.get_device_name(0),
                "gpu_memory_gb": round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2),
                "cuda_version": torch.version.cuda
            })
        
        return info
    
    def load_model_and_tokenizer(self, model_path: Optional[str] = None):
        """
        Load tokenizer and model.
        
        Args:
            model_path: Path to saved model, or None to load pre-trained model
        """
        if model_path and Path(model_path).exists():
            logger.info(f"Loading fine-tuned model from {model_path}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        else:
            logger.info(f"Loading pre-trained model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name, 
                num_labels=self.num_labels
            )
        
        self.model.to(self.device)
        
        # Add padding token if it doesn't exist
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
    
    def prepare_dataset(self, df: pd.DataFrame, test_size: float = 0.2) -> Tuple[Dataset, Dataset]:
        """
        Prepare dataset for training.
        
        Args:
            df: DataFrame with 'text' and 'label' columns
            test_size: Fraction of data to use for validation
            
        Returns:
            Tuple of (train_dataset, val_dataset)
        """
        # Split the data
        train_df, val_df = train_test_split(
            df, 
            test_size=test_size, 
            random_state=self.random_state,
            stratify=df['label']
        )
        
        logger.info(f"Training samples: {len(train_df)}")
        logger.info(f"Validation samples: {len(val_df)}")
        
        # Convert to datasets
        train_dataset = Dataset.from_pandas(train_df)
        val_dataset = Dataset.from_pandas(val_df)
        
        # Remove any index columns that pandas might have added
        train_dataset = train_dataset.remove_columns([col for col in train_dataset.column_names if col not in ['text', 'label']])
        val_dataset = val_dataset.remove_columns([col for col in val_dataset.column_names if col not in ['text', 'label']])
        
        # Tokenize with proper column handling
        train_dataset = train_dataset.map(
            self._tokenize_function, 
            batched=True,
            remove_columns=['text']  # Remove text column after tokenization
        )
        val_dataset = val_dataset.map(
            self._tokenize_function, 
            batched=True,
            remove_columns=['text']  # Remove text column after tokenization  
        )
        
        return train_dataset, val_dataset
    
    def _tokenize_function(self, examples):
        """Tokenize text examples."""
        # Handle both single examples and batched examples
        if isinstance(examples["text"], list):
            texts = examples["text"]
        else:
            texts = [examples["text"]]
        
        # Tokenize with proper settings
        tokenized = self.tokenizer(
            texts,
            truncation=True,
            padding=False,  # Padding will be done dynamically by data collator
            max_length=self.max_length,
            return_tensors=None  # Return lists, not tensors
        )
        
        return tokenized
    
    def compute_metrics(self, eval_pred):
        """Compute metrics for evaluation."""
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        return {
            'accuracy': accuracy_score(labels, predictions)
        }
    
    def train_model(self, 
                   train_dataset: Dataset, 
                   val_dataset: Dataset,
                   output_dir: str = "models/bert_sentiment",
                   epochs: int = 3,
                   batch_size: int = 16,
                   learning_rate: float = 2e-5,
                   warmup_steps: int = 500,
                   weight_decay: float = 0.01) -> Dict[str, Any]:
        """
        Train the BERT model.
        
        Args:
            train_dataset: Training dataset
            val_dataset: Validation dataset
            output_dir: Directory to save the model
            epochs: Number of training epochs
            batch_size: Training batch size
            learning_rate: Learning rate
            warmup_steps: Number of warmup steps
            weight_decay: Weight decay for regularization
            
        Returns:
            Dictionary with training metrics and info
        """
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Training arguments with early stopping
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            warmup_steps=warmup_steps,
            weight_decay=weight_decay,
            learning_rate=learning_rate,
            logging_dir=f"{output_dir}/logs",
            logging_steps=50,
            eval_strategy="steps",
            eval_steps=200,
            save_strategy="steps", 
            save_steps=200,
            load_best_model_at_end=True,
            metric_for_best_model="eval_accuracy",
            greater_is_better=True,
            save_total_limit=3,
            # Performance optimizations
            dataloader_num_workers=0,  # Disable for Windows compatibility
            remove_unused_columns=False,
            push_to_hub=False,
            report_to=[],  # Disable wandb/tensorboard unless configured
        )
        
        # Data collator
        data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer)
        
        # Initialize trainer with early stopping
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            processing_class=self.tokenizer,  # Updated from deprecated 'tokenizer'
            data_collator=data_collator,
            compute_metrics=self.compute_metrics,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=3, early_stopping_threshold=0.001)]
        )
        
        # Record training start time and resources
        start_time = time.time()
        device_info = self._get_device_info()
        
        logger.info(f"Starting training on {device_info['device']}")
        logger.info(f"Training samples: {len(train_dataset)}")
        logger.info(f"Validation samples: {len(val_dataset)}")
        logger.info(f"Epochs: {epochs}, Batch size: {batch_size}")
        
        # Train the model
        try:
            train_result = trainer.train()
            
            # Save the model
            trainer.save_model()
            self.tokenizer.save_pretrained(output_dir)
            
            training_time = time.time() - start_time
            
            # Get final evaluation metrics
            eval_result = trainer.evaluate()
            
            # Prepare training summary
            training_summary = {
                "model_name": self.model_name,
                "training_samples": len(train_dataset),
                "validation_samples": len(val_dataset),
                "epochs": epochs,
                "batch_size": batch_size,
                "learning_rate": learning_rate,
                "training_time_seconds": round(training_time, 2),
                "training_time_minutes": round(training_time / 60, 2),
                "final_train_loss": train_result.training_loss,
                "final_eval_accuracy": eval_result["eval_accuracy"],
                "final_eval_loss": eval_result["eval_loss"],
                "device_info": device_info,
                "output_dir": output_dir
            }
            
            logger.info(f"Training completed in {training_summary['training_time_minutes']:.2f} minutes")
            logger.info(f"Final validation accuracy: {training_summary['final_eval_accuracy']:.4f}")
            
            return training_summary
            
        except Exception as e:
            logger.error(f"Training failed: {str(e)}")
            raise
    
    def predict(self, texts: list, model_path: str) -> Tuple[list, list]:
        """
        Make predictions on new texts.
        
        Args:
            texts: List of texts to classify
            model_path: Path to the trained model
            
        Returns:
            Tuple of (predictions, probabilities)
        """
        # Load model if not already loaded or if different path
        if self.model is None:
            self.load_model_and_tokenizer(model_path)
        
        self.model.eval()
        predictions = []
        probabilities = []
        
        with torch.no_grad():
            for text in texts:
                # Tokenize
                inputs = self.tokenizer(
                    text,
                    return_tensors="pt",
                    truncation=True,
                    padding=True,
                    max_length=self.max_length
                ).to(self.device)
                
                # Get prediction
                outputs = self.model(**inputs)
                logits = outputs.logits
                
                # Convert to probabilities
                probs = torch.softmax(logits, dim=-1)
                
                # Get prediction
                pred = torch.argmax(logits, dim=-1).item()
                prob = probs.max().item()
                
                predictions.append(pred)
                probabilities.append(prob)
        
        return predictions, probabilities
    
    def predict_single(self, text: str) -> int:
        """
        Predict sentiment for a single text string.
        
        Args:
            text: Input text to classify
            
        Returns:
            Predicted sentiment label (0=negative, 1=neutral, 2=positive)
        """
        if not self.model or not self.tokenizer:
            raise ValueError("Model and tokenizer must be loaded first")
        
        # Tokenize input
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=self.max_length
        )
        
        # Move to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Predict
        self.model.eval()
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.argmax(outputs.logits, dim=-1)
            
        return predictions.cpu().numpy()[0]
    
    def evaluate_model(self, df: pd.DataFrame, model_path: str) -> Dict[str, Any]:
        """
        Evaluate model on test dataset.
        
        Args:
            df: DataFrame with 'text' and 'label' columns
            model_path: Path to the trained model
            
        Returns:
            Dictionary with evaluation metrics
        """
        start_time = time.time()
        
        # Make predictions
        predictions, probabilities = self.predict(df['text'].tolist(), model_path)
        
        # Calculate metrics
        accuracy = accuracy_score(df['label'], predictions)
        
        # Classification report
        class_report = classification_report(
            df['label'], 
            predictions, 
            target_names=['Negative', 'Neutral', 'Positive'],
            output_dict=True
        )
        
        # Confusion matrix
        conf_matrix = confusion_matrix(df['label'], predictions)
        
        inference_time = time.time() - start_time
        
        evaluation_results = {
            "model_path": model_path,
            "test_samples": len(df),
            "accuracy": accuracy,
            "inference_time_seconds": round(inference_time, 2),
            "samples_per_second": round(len(df) / inference_time, 2),
            "classification_report": class_report,
            "confusion_matrix": conf_matrix.tolist(),
            "predictions": predictions,
            "probabilities": probabilities,
            "device_info": self._get_device_info()
        }
        
        logger.info(f"Evaluation completed in {inference_time:.2f} seconds")
        logger.info(f"Test accuracy: {accuracy:.4f}")
        logger.info(f"Inference speed: {evaluation_results['samples_per_second']:.2f} samples/sec")
        
        return evaluation_results
