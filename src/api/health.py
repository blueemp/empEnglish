"""Health check router."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", status_code=200)
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0", "service": "empEnglish"}


@router.get("/", status_code=200)
async def root():
    """Root endpoint."""
    return {
        "service": "empEnglish",
        "description": "AI-powered English oral practice platform",
        "version": "1.0.0",
        "docs": "/docs",
    }
