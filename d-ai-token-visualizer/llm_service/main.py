"""Main FastAPI application for Local LLM Service."""

import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings
from models.gemma_model import GemmaModelManager
from api.routes import router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global model manager instance
model_manager: GemmaModelManager = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - startup and shutdown events."""
    global model_manager
    
    # Startup
    logger.info("🚀 Starting Local LLM Service...")
    logger.info(f"📋 Model: {settings.model_name}")
    logger.info(f"🔧 Device: {settings.device}")
    logger.info(f"⚡ Quantization: {settings.quantization or 'None'}")
    
    try:
        # Initialize model manager
        model_manager = GemmaModelManager()
        
        # Load model in background task to avoid blocking startup
        asyncio.create_task(model_manager.initialize_async())
        
        logger.info("✅ Service started successfully")
        logger.info(f"🌐 Listening on {settings.host}:{settings.port}")
        
    except Exception as e:
        logger.error(f"❌ Failed to start service: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Local LLM Service...")
    if model_manager:
        model_manager.cleanup()
    logger.info("👋 Service stopped")


# Create FastAPI application
app = FastAPI(
    title="Local LLM Service",
    description="FastAPI service for local LLM token generation using Gemma 2 2B",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Reflex app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "Local LLM Service",
        "version": "1.0.0",
        "model": settings.model_name,
        "status": "running"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    global model_manager
    
    if not model_manager:
        raise HTTPException(status_code=503, detail="Model manager not initialized")
    
    is_ready = model_manager.is_ready()
    
    return {
        "status": "healthy" if is_ready else "initializing",
        "model_ready": is_ready,
        "timestamp": asyncio.get_event_loop().time()
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )


# Make model manager available to routes
def get_model_manager() -> GemmaModelManager:
    """Get the global model manager instance."""
    global model_manager
    if not model_manager:
        raise HTTPException(status_code=503, detail="Model manager not initialized")
    return model_manager


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level,
        access_log=True
    )
