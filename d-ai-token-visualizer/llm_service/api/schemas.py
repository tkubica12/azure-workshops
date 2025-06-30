"""Pydantic schemas for API request/response validation."""

from typing import List, Optional
from pydantic import BaseModel, Field


class TokenProbabilitySchema(BaseModel):
    """Schema for token probability information."""
    token: str = Field(..., description="The token text")
    logprob: float = Field(..., description="Log probability of the token")
    probability: float = Field(..., description="Probability of the token (0-1 range)")
    percentage: float = Field(..., description="Probability as percentage (0-100 range)")


class GenerationRequest(BaseModel):
    """Request schema for token generation."""
    prompt: str = Field(..., description="Input text prompt", min_length=1, max_length=2048)
    max_tokens: Optional[int] = Field(1, description="Number of tokens to generate", ge=1, le=100)
    temperature: Optional[float] = Field(0.7, description="Sampling temperature", ge=0.0, le=2.0)
    top_logprobs: Optional[int] = Field(5, description="Number of top alternatives to return", ge=1, le=20)


class GenerationResponse(BaseModel):
    """Response schema for token generation."""
    prompt: str = Field(..., description="The original prompt")
    generated_text: str = Field(..., description="The complete generated text")
    selected_token: TokenProbabilitySchema = Field(..., description="The selected token with probability")
    top_alternatives: List[TokenProbabilitySchema] = Field(..., description="Top alternative tokens")
    generation_time: float = Field(..., description="Time taken for generation in seconds")
    model_name: str = Field(..., description="Name of the model used")


class HealthResponse(BaseModel):
    """Response schema for health check."""
    status: str = Field(..., description="Service status")
    model_ready: bool = Field(..., description="Whether the model is ready for inference")
    timestamp: float = Field(..., description="Timestamp of the health check")


class StatusResponse(BaseModel):
    """Response schema for service status."""
    status: str = Field(..., description="Service status")
    model_name: str = Field(..., description="Name of the loaded model")
    device: str = Field(..., description="Device used for inference")
    quantization: bool = Field(..., description="Whether quantization is enabled")
    parameters_billions: Optional[float] = Field(None, description="Model parameters in billions")
    memory_efficient: bool = Field(..., description="Whether memory efficiency is enabled")


class TestResponse(BaseModel):
    """Response schema for model test."""
    status: str = Field(..., description="Test status")
    prompt: Optional[str] = Field(None, description="Test prompt used")
    selected_token: Optional[str] = Field(None, description="Selected token from test")
    selected_probability: Optional[str] = Field(None, description="Probability of selected token")
    top_alternatives: Optional[List[dict]] = Field(None, description="Top alternative tokens")
    generation_time: Optional[str] = Field(None, description="Time taken for generation")
    message: Optional[str] = Field(None, description="Error message if test failed")


class ErrorResponse(BaseModel):
    """Response schema for errors."""
    detail: str = Field(..., description="Error description")
    error_type: Optional[str] = Field(None, description="Type of error")
    timestamp: Optional[float] = Field(None, description="Timestamp of the error")
