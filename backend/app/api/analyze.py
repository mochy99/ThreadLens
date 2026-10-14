
from fastapi import APIRouter, HTTPException, Query
from fastapi.concurrency import run_in_threadpool

from app.api.posts import load_posts
from app.services.llm_analyzer import analyze_with_llm

router = APIRouter(
    prefix="/api/analyze",
    tags=["AI Analysis"],
)


@router.get("")
async def analyze_all_posts(
    limit: int = Query(default=5, ge=1, le=20),
):
    posts = load_posts()
    selected = posts[:limit]

    results = []

    for post in selected:
        result = await run_in_threadpool(
            analyze_with_llm,
            post,
        )
        results.append(result)

    return {
        "total": len(results),
        "results": results,
    }


@router.get("/{post_id}")
async def analyze_single_post(post_id: str):
    posts = load_posts()

    for post in posts:
        if str(post.get("id")) == post_id:
            return await run_in_threadpool(
                analyze_with_llm,
                post,
            )

    raise HTTPException(
        status_code=404,
        detail="Discussion not found",
    )
