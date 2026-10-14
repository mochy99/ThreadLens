
from pathlib import Path
import json
from typing import Any

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/api/posts", tags=["Posts"])

DATA_PATH = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "piazza_posts.json"
)


def load_posts() -> list[dict[str, Any]]:
    """Load synthetic Piazza discussions from JSON."""
    if not DATA_PATH.exists():
        raise HTTPException(
            status_code=503,
            detail="Discussion dataset is unavailable.",
        )

    try:
        with DATA_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to load discussion dataset.",
        ) from exc

    if not isinstance(data, list):
        raise HTTPException(
            status_code=500,
            detail="Dataset must contain a list of posts.",
        )

    return data


@router.get("")
def get_posts(
    search: str | None = Query(
        default=None,
        description="Search titles and discussion content",
    ),
    course: str | None = None,
    status: str | None = None,
    tag: str | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
):
    """
    Retrieve discussions with optional filtering,
    keyword search, and pagination.
    """
    posts = load_posts()

    if search:
        keyword = search.casefold()
        posts = [
            post for post in posts
            if keyword in str(post.get("title", "")).casefold()
            or keyword in str(post.get("content", "")).casefold()
        ]

    if course:
        posts = [
            post for post in posts
            if str(post.get("course", "")).casefold()
            == course.casefold()
        ]

    if status:
        posts = [
            post for post in posts
            if str(post.get("status", "")).casefold()
            == status.casefold()
        ]

    if tag:
        posts = [
            post for post in posts
            if tag.casefold() in [
                str(t).casefold()
                for t in post.get("tags", [])
            ]
        ]

    total = len(posts)

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "posts": posts[skip : skip + limit],
    }


@router.get("/{post_id}")
def get_post(post_id: str):
    """Retrieve a single discussion by ID."""
    posts = load_posts()

    for post in posts:
        if str(post.get("id")) == post_id:
            return post

    raise HTTPException(
        status_code=404,
        detail=f"Post '{post_id}' not found.",
    )
