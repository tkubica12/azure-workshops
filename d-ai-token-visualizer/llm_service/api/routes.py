"""API routes for the LLM service."""

import asyncio
import time
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from .schemas import (
    GenerationRequest, GenerationResponse, HealthResponse, 
    StatusResponse, TestResponse, ErrorResponse, TokenProbabilitySchema
)
from models.gemma_model import GemmaModelManager
from config import settings

# Create router
router = APIRouter()

# Dependency to get model manager
async def get_model_manager() -> GemmaModelManager:
    """Dependency to get the model manager."""
    # Import here to avoid circular imports
    from main import get_model_manager
    return get_model_manager()


@router.get("/health", response_model=HealthResponse)
async def health_check(model_manager: GemmaModelManager = Depends(get_model_manager)):
    """Health check endpoint."""
    is_ready = model_manager.is_ready()
    
    return HealthResponse(
        status="healthy" if is_ready else "initializing",
        model_ready=is_ready,
        timestamp=time.time()
    )


@router.get("/status", response_model=StatusResponse)
async def get_status(model_manager: GemmaModelManager = Depends(get_model_manager)):
    """Get service and model status information."""
    model_info = model_manager.get_model_info()
    
    return StatusResponse(
        status=model_info["status"],
        model_name=model_info["model_name"],
        device=model_info.get("device", "unknown"),
        quantization=model_info["quantization"],
        parameters_billions=model_info.get("parameters_billions"),
        memory_efficient=model_info.get("memory_efficient", False)
    )


@router.post("/test", response_model=TestResponse)
async def test_generation(model_manager: GemmaModelManager = Depends(get_model_manager)):
    """Test the model with a simple generation."""
    if not model_manager.is_ready():
        raise HTTPException(
            status_code=503, 
            detail="Model not ready. Please wait for initialization to complete."
        )
    
    try:
        result = await model_manager.test_generation()
        
        if result["status"] == "success":
            return TestResponse(
                status="success",
                prompt=result["prompt"],
                selected_token=result["selected_token"],
                selected_probability=result["selected_probability"],
                top_alternatives=result["top_alternatives"],
                generation_time=result["generation_time"]
            )
        else:
            return TestResponse(
                status="error",
                message=result["message"]
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")


@router.post("/generate", response_model=GenerationResponse)
async def generate_tokens(
    request: GenerationRequest,
    model_manager: GemmaModelManager = Depends(get_model_manager)
):
    """Generate tokens with probability information."""
    if not model_manager.is_ready():
        raise HTTPException(
            status_code=503, 
            detail="Model not ready. Please wait for initialization to complete."
        )
    
    # Validate request parameters
    if len(request.prompt) > settings.max_prompt_length:
        raise HTTPException(
            status_code=400,
            detail=f"Prompt too long. Maximum length is {settings.max_prompt_length} characters."
        )
    
    try:
        # Generate tokens with probabilities
        result = await model_manager.generate_with_logprobs(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_logprobs=request.top_logprobs
        )
        
        # Convert to response schema
        selected_token_schema = TokenProbabilitySchema(
            token=result.selected_token.token,
            logprob=result.selected_token.logprob,
            probability=result.selected_token.probability,
            percentage=result.selected_token.percentage
        )
        
        top_alternatives_schema = [
            TokenProbabilitySchema(
                token=alt.token,
                logprob=alt.logprob,
                probability=alt.probability,
                percentage=alt.percentage
            )
            for alt in result.top_alternatives
        ]
        
        return GenerationResponse(
            prompt=request.prompt,
            generated_text=result.generated_text,
            selected_token=selected_token_schema,
            top_alternatives=top_alternatives_schema,
            generation_time=result.generation_time,
            model_name=settings.model_name
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
