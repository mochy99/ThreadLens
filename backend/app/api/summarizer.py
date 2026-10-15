from fastapi import APIRouter, HTTPException
from starlette.concurrency import run_in_threadpool

from app.api.posts import load_posts
from app.services.summarizer import generate_summary

router = APIRouter(
    prefix="/api/summarizer",
    tags=["Summarizer"],
)


@router.get("/courses")
def get_available_courses():
    posts = load_posts()

    courses = sorted({
        str(post["course"])
        for post in posts
        if post.get("course")
    })

    return {"courses": courses}


@router.get("/{course}")
async def summarize_course(course: str):
    posts = load_posts()

    try:
        return await run_in_threadpool(
            generate_summary,
            posts,
            course,
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))