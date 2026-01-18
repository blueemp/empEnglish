"""Main FastAPI application entry point."""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.utils.config import settings
from src.api import health, auth, users, questions, practice

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered English oral practice platform for Chinese graduate school entrance exams",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="", tags=["Health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(questions.router, prefix="/api/v1/questions", tags=["Questions"])
app.include_router(practice.router, prefix="/api/v1/practice", tags=["Practice"])


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    from src.utils.database import init_db

    init_db()
    print(f"{settings.APP_NAME} v{settings.APP_VERSION} started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    print(f"{settings.APP_NAME} shutting down")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
