
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Query

from app.api.posts import load_posts

router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"],
)


def filter_by_course(
    posts: list[dict[str, Any]],
    course: str | None,
) -> list[dict[str, Any]]:
    """Filter discussions by course."""
    if not course:
        return posts

    return [
        post for post in posts
        if str(post.get("course", "")).casefold()
        == course.casefold()
    ]


def get_status(post: dict[str, Any]) -> str:
    """Normalize a discussion's resolution status."""
    status = str(post.get("status", "")).strip().lower()

    if status in {"resolved", "unresolved", "in_progress"}:
        return status

    if status in {"in progress", "open"}:
        return (
            "in_progress"
            if status == "in progress"
            else "unresolved"
        )

    if post.get("is_resolved") is True:
        return "resolved"

    if post.get("is_resolved") is False:
        return "unresolved"

    return "unknown"


def parse_timestamp(value: Any) -> datetime | None:
    """Parse an ISO 8601 timestamp safely."""
    if not isinstance(value, str):
        return None

    try:
        timestamp = datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(
                tzinfo=timezone.utc
            )

        return timestamp.astimezone(timezone.utc)

    except ValueError:
        return None


@router.get("")
def get_analytics(
    course: str | None = Query(default=None),
):
    """
    Return overview statistics for the dashboard.
    """
    posts = filter_by_course(load_posts(), course)

    status_counts = Counter(
        get_status(post) for post in posts
    )

    total = len(posts)
    resolved = status_counts["resolved"]
    unresolved = status_counts["unresolved"]
    in_progress = status_counts["in_progress"]

    resolution_rate = (
        round(resolved / total * 100, 2)
        if total > 0
        else 0.0
    )

    return {
        "total_posts": total,
        "resolved": resolved,
        "unresolved": unresolved,
        "in_progress": in_progress,
        "unknown": status_counts["unknown"],
        "resolution_rate": resolution_rate,
    }


@router.get("/topics")
def get_topic_analytics(
    course: str | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
):
    """
    Count the most frequently used discussion tags.
    """
    posts = filter_by_course(load_posts(), course)

    topic_counts = Counter()

    for post in posts:
        tags = post.get("tags", [])

        if not isinstance(tags, list):
            continue

        for tag in set(
            str(tag).strip().lower()
            for tag in tags
            if str(tag).strip()
        ):
            topic_counts[tag] += 1

    topics = [
        {"topic": topic, "count": count}
        for topic, count in topic_counts.most_common(limit)
    ]

    return {
        "total_topics": len(topic_counts),
        "topics": topics,
    }


@router.get("/trends")
def get_discussion_trends(
    course: str | None = Query(default=None),
    interval: str = Query(
        default="day",
        pattern="^(day|week|month)$",
    ),
):
    """
    Count discussion posts over time.

    Supported intervals:
    - day
    - week
    - month
    """
    posts = filter_by_course(load_posts(), course)

    trends = defaultdict(
        lambda: {
            "total": 0,
            "resolved": 0,
            "unresolved": 0,
            "in_progress": 0,
        }
    )

    for post in posts:
        timestamp = parse_timestamp(
            post.get("created_at")
        )

        if timestamp is None:
            continue

        if interval == "day":
            period = timestamp.strftime("%Y-%m-%d")

        elif interval == "week":
            year, week, _ = timestamp.isocalendar()
            period = f"{year}-W{week:02d}"

        else:
            period = timestamp.strftime("%Y-%m")

        status = get_status(post)

        trends[period]["total"] += 1

        if status in trends[period]:
            trends[period][status] += 1

    return {
        "interval": interval,
        "trends": [
            {
                "period": period,
                **counts,
            }
            for period, counts in sorted(trends.items())
        ],
    }


@router.get("/courses")
def get_course_analytics():
    """
    Return discussion counts and resolution rates
    grouped by course.
    """
    posts = load_posts()

    grouped = defaultdict(list)

    for post in posts:
        course = str(
            post.get("course") or "Unknown"
        )
        grouped[course].append(post)

    results = []

    for course, course_posts in sorted(grouped.items()):
        total = len(course_posts)

        resolved = sum(
            get_status(post) == "resolved"
            for post in course_posts
        )

        results.append({
            "course": course,
            "total_posts": total,
            "resolved": resolved,
            "unresolved": sum(
                get_status(post) == "unresolved"
                for post in course_posts
            ),
            "resolution_rate": round(
                resolved / total * 100, 2
            ) if total else 0.0,
        })

    return {
        "total_courses": len(results),
        "courses": results,
    }


@router.get("/unresolved")
def get_unresolved_analytics(
    course: str | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
):
    """
    Retrieve unresolved discussions for dashboard review.
    """
    posts = filter_by_course(load_posts(), course)

    unresolved = [
        post for post in posts
        if get_status(post) == "unresolved"
    ]

    unresolved.sort(
        key=lambda post: (
            parse_timestamp(post.get("created_at"))
            or datetime.min.replace(tzinfo=timezone.utc)
        ),
        reverse=True,
    )

    return {
        "total_unresolved": len(unresolved),
        "posts": unresolved[:limit],
    }
