from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.posts import router as posts_router
from app.api.analytics import router as analytics_router
from app.api.analyze import router as analyze_router
from app.api import summarizer





app = FastAPI(
    title="ThreadLens API",
    description="AI-Powered Discussion Analytics Platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(posts_router)
app.include_router(analytics_router)
app.include_router(analyze_router)
app.include_router(summarizer.router)


@app.get("/")
def health_check():
    return {
        "message": "ThreadLens API is running",
        "version": "0.1.0",
    }
