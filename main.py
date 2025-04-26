import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.routes import api_router
from config.settings import settings
from utils.logging_utils import setup_logging

# Setup logging
logger = setup_logging()

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# Include API routes
app.include_router(api_router)

@app.get("/")
async def root():
    """Root endpoint that returns a welcome message."""
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the RAG API with web crawling capabilities and conversation memory"}

# Global exception handler - this needs to be on the app, not router
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle any uncaught exceptions across API routes."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status_code": 500,
            "message": "Internal server error",
            "details": str(exc)
        }
    )

if __name__ == "__main__":
    logger.info(f"Starting {settings.APP_TITLE} on port {settings.PORT}")
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)