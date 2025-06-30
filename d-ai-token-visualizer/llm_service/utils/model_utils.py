"""Utility functions for the LLM service."""

import logging
from typing import Dict, Any


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ]
    )
    return logging.getLogger(__name__)


def format_model_info(model_info: Dict[str, Any]) -> str:
    """Format model information for display."""
    if model_info["status"] != "ready":
        return f"Model: {model_info['model_name']} (Status: {model_info['status']})"
    
    return (
        f"Model: {model_info['model_name']} "
        f"({model_info.get('parameters_billions', 'Unknown')}B parameters, "
        f"Device: {model_info['device']}, "
        f"Quantization: {'Enabled' if model_info['quantization'] else 'Disabled'})"
    )
