"""
Training utilities for logistic regression models on embeddings.
Supports CPU training with resource monitoring.
"""

import os
import time
import pickle
import logging
from typing import Tuple, Dict, Any
from datetime import datetime

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import psutil

logger = logging.getLogger(__name__)


class TrainingUtils:
    """Utility class for training logistic regression models on embeddings."""
    
    def __init__(self, 
                 random_state: int = 42,
                 test_size: float = 0.2,
                 use_gpu: bool = True,
                 max_iter: int = 1000):
        """
        Initialize training utilities.
        
        Args:
            random_state: Random seed for reproducibility
            test_size: Fraction of data to use for testing
            use_gpu: Whether to attempt GPU acceleration (currently CPU-only)
            max_iter: Maximum iterations for logistic regression
        """
        self.random_state = random_state
        self.test_size = test_size
        self.use_gpu = use_gpu
        self.max_iter = max_iter
        
        # Check for GPU availability (currently disabled for compatibility)
        self.gpu_available = False  # Simplified for now
        self.device_info = self._get_device_info()
        
        logger.info(f"Training utilities initialized")
        logger.info(f"GPU available: {self.gpu_available}")
        logger.info(f"Device info: {self.device_info}")
    
    def _get_device_info(self) -> Dict[str, Any]:
        """Get information about available compute devices."""
        info = {
            'cpu_count': psutil.cpu_count(),
            'memory_gb': round(psutil.virtual_memory().total / (1024**3), 2),
            'gpu_available': self.gpu_available
        }
        return info
    
    def load_embedding_data(self, data_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load embedding data from parquet file.
        
        Args:
            data_path: Path to parquet file with embeddings
            
        Returns:
            Tuple of (embeddings_array, labels_array)
        """
        logger.info(f"Loading data from {data_path}")
        
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data file not found: {data_path}")
        
        # Load the parquet file
        df = pd.read_parquet(data_path)
        logger.info(f"Loaded {len(df)} samples from {data_path}")
        
        # Extract embeddings and labels
        if 'embedding' in df.columns:
            # Embeddings are stored as arrays in a single column
            embeddings = np.array(df['embedding'].tolist())
        else:
            raise ValueError("No 'embedding' column found in data")
        
        if 'label' in df.columns:
            labels = df['label'].values
        else:
            raise ValueError("No 'label' column found in data")
        
        logger.info(f"Embeddings shape: {embeddings.shape}")
        logger.info(f"Labels shape: {labels.shape}")
        logger.info(f"Unique labels: {np.unique(labels)}")
        
        return embeddings, labels
    
    def create_model(self) -> LogisticRegression:
        """
        Create a logistic regression model.
        
        Returns:
            Logistic regression model instance        """
        model = LogisticRegression(
            random_state=self.random_state,
            max_iter=self.max_iter,
            n_jobs=-1  # Use all CPU cores
        )
        logger.info("Created sklearn CPU logistic regression model")
        return model
    
    def train_model(self, 
                   data_path: str,
                   model_output_path: str,
                   stats_output_path: str) -> Dict[str, Any]:
        """
        Train a logistic regression model on embedding data.
        
        Args:
            data_path: Path to training data (parquet)
            model_output_path: Path to save trained model
            stats_output_path: Path to save training statistics
            
        Returns:
            Dictionary with training results and statistics
        """
        training_start_time = time.time()
        process_start = psutil.Process()
        memory_start = process_start.memory_info().rss / (1024**2)  # MB
        
        logger.info("="*60)
        logger.info(f"STARTING LOGISTIC REGRESSION TRAINING")
        logger.info("="*60)
        logger.info(f"Data path: {data_path}")
        logger.info(f"Model output: {model_output_path}")
        logger.info(f"Stats output: {stats_output_path}")
        # Print initial training info
        print(f"\n🚀 Starting logistic regression training...")
        print(f"📁 Data: {data_path}")
        print(f"💾 Model output: {model_output_path}")
        print(f"📊 Stats output: {stats_output_path}")
        
        try:
            # Load data
            X, y = self.load_embedding_data(data_path)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, 
                test_size=self.test_size, 
                random_state=self.random_state,
                stratify=y
            )
            
            logger.info(f"Training set: {X_train.shape[0]} samples")
            logger.info(f"Test set: {X_test.shape[0]} samples")
            
            # Create and train model
            model = self.create_model()
            
            # Time the actual training
            train_start_time = time.time()
            logger.info("Starting model training...")
            
            model.fit(X_train, y_train)
            
            train_end_time = time.time()
            training_time = train_end_time - train_start_time
            
            logger.info(f"Model training completed in {training_time:.2f} seconds")
            
            # Make predictions
            logger.info("Making predictions on test set...")
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            
            # Generate classification report
            class_report = classification_report(y_test, y_pred, output_dict=True)
            conf_matrix = confusion_matrix(y_test, y_pred)
            
            # Calculate resource usage
            memory_end = psutil.Process().memory_info().rss / (1024**2)  # MB
            memory_used = memory_end - memory_start
            total_time = time.time() - training_start_time
            
            # Prepare results
            results = {
                'model_path': model_output_path,
                'data_path': data_path,
                'dataset_size': len(X),
                'embedding_dimensions': X.shape[1],
                'train_size': len(X_train),
                'test_size': len(X_test),
                'test_accuracy': accuracy,
                'training_time_seconds': training_time,
                'total_time_seconds': total_time,
                'memory_used_mb': memory_used,
                'device_used': 'CPU (sklearn)',
                'device_info': self.device_info,
                'classification_report': class_report,
                'confusion_matrix': conf_matrix.tolist(),
                'model_type': 'LogisticRegression',
                'random_state': self.random_state,
                'max_iter': self.max_iter,
                'timestamp': datetime.now().isoformat()
            }
            
            # Save model
            logger.info(f"Saving model to {model_output_path}")
            os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
            
            with open(model_output_path, 'wb') as f:
                pickle.dump(model, f)
            
            # Save statistics
            self._save_training_stats(results, stats_output_path)
            
            # Print summary
            self._print_training_summary(results)
            
            return results
            
        except Exception as e:
            logger.error(f"Training failed: {str(e)}")
            raise
    
    def _save_training_stats(self, results: Dict[str, Any], stats_path: str):
        """Save training statistics to text file."""
        os.makedirs(os.path.dirname(stats_path), exist_ok=True)
        
        with open(stats_path, 'w') as f:
            f.write("LOGISTIC REGRESSION TRAINING STATISTICS\n")
            f.write("="*60 + "\n\n")
            
            # Basic info
            f.write(f"Timestamp: {results['timestamp']}\n")
            f.write(f"Data Path: {results['data_path']}\n")
            f.write(f"Model Path: {results['model_path']}\n\n")
            
            # Dataset info
            f.write("DATASET INFORMATION:\n")
            f.write(f"  Total samples: {results['dataset_size']:,}\n")
            f.write(f"  Embedding dimensions: {results['embedding_dimensions']:,}\n")
            f.write(f"  Training samples: {results['train_size']:,}\n")
            f.write(f"  Test samples: {results['test_size']:,}\n\n")
            
            # Performance metrics
            f.write("PERFORMANCE METRICS:\n")
            f.write(f"  Test Accuracy: {results['test_accuracy']:.4f}\n\n")
            
            # Resource usage
            f.write("RESOURCE USAGE:\n")
            f.write(f"  Device Used: {results['device_used']}\n")
            f.write(f"  Training Time: {results['training_time_seconds']:.2f} seconds\n")
            f.write(f"  Total Time: {results['total_time_seconds']:.2f} seconds\n")
            f.write(f"  Memory Used: {results['memory_used_mb']:.1f} MB\n\n")
            
            # Device info
            f.write("DEVICE INFORMATION:\n")
            for key, value in results['device_info'].items():
                f.write(f"  {key}: {value}\n")
            f.write("\n")
            
            # Model configuration
            f.write("MODEL CONFIGURATION:\n")
            f.write(f"  Model Type: {results['model_type']}\n")
            f.write(f"  Random State: {results['random_state']}\n")
            f.write(f"  Max Iterations: {results['max_iter']}\n\n")
            
            # Classification report
            f.write("CLASSIFICATION REPORT:\n")
            if 'classification_report' in results:
                for label, metrics in results['classification_report'].items():
                    if isinstance(metrics, dict):
                        f.write(f"  {label}:\n")
                        for metric, value in metrics.items():
                            if isinstance(value, (int, float)):
                                f.write(f"    {metric}: {value:.4f}\n")
            
            # Confusion matrix
            f.write(f"\nCONFUSION MATRIX:\n")
            conf_matrix = np.array(results['confusion_matrix'])
            f.write(str(conf_matrix))
        
        logger.info(f"Training statistics saved to {stats_path}")
    
    def _print_training_summary(self, results: Dict[str, Any]):
        """Print a summary of training results."""
        print("\n" + "="*60)
        print("TRAINING COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"📊 Dataset: {results['dataset_size']:,} samples, {results['embedding_dimensions']:,} dimensions")
        print(f"🎯 Accuracy: {results['test_accuracy']:.4f}")
        print(f"⚡ Training Time: {results['training_time_seconds']:.2f} seconds")
        print(f"💻 Device: {results['device_used']}")
        print(f"💾 Memory Used: {results['memory_used_mb']:.1f} MB")
        print(f"📁 Model saved to: {results['model_path']}")
        print("="*60)
    
    def load_model(self, model_path: str):
        """
        Load a trained model from file.
        
        Args:
            model_path: Path to saved model
            
        Returns:
            Loaded model instance
        """
        logger.info(f"Loading model from {model_path}")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        logger.info("Model loaded successfully")
        return model