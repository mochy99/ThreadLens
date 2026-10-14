import re
from collections import Counter
from typing import Any


TOPIC_KEYWORDS = {
    "assignments": [
        "assignment", "homework", "deadline",
        "submission", "grading", "autograder",
    ],
    "exams": [
        "exam", "midterm", "final", "quiz",
        "cheat sheet", "practice test",
    ],
    "debugging": [
        "error", "bug", "debug", "exception",
        "traceback", "segmentation fault",
        "not working", "failed test",
    ],
    "lectures": [
        "lecture", "slides", "concept",
        "theorem", "proof", "algorithm",
    ],
    "course_admin": [
        "office hours", "schedule", "piazza",
        "registration", "section", "syllabus",
    ],
}

URGENT_KEYWORDS = [
    "urgent", "asap", "immediately",
    "deadline today", "due tonight",
    "cannot submit", "blocked",
]

MEDIUM_KEYWORDS = [
    "error", "failed", "stuck", "confused",
    "not working", "help", "issue",
]

STOPWORDS = {
    "the", "and", "for", "with", "that",
    "this", "from", "have", "what", "when",
    "where", "why", "how", "are", "was",
    "were", "can", "could", "would",
    "should", "about", "into", "your",
    "you", "our", "their", "they", "but",
}


def normalize_text(text: str) -> str:
    """Normalize whitespace without changing meaning."""
    return re.sub(r"\s+", " ", text).strip()


def extract_message_text(messages: Any) -> str:
    """
    Extract text from answers or follow-ups.

    Supports lists of strings or dictionaries.
    """
    if not isinstance(messages, list):
        return ""

    parts = []

    for message in messages:
        if isinstance(message, str):
            parts.append(message)

        elif isinstance(message, dict):
            for key in ("content", "text", "body"):
                value = message.get(key)

                if isinstance(value, str):
                    parts.append(value)
                    break

    return " ".join(parts)


def get_discussion_text(post: dict[str, Any]) -> str:
    """Combine all available discussion content."""
    parts = [
        str(post.get("title") or ""),
        str(post.get("content") or ""),
        extract_message_text(post.get("answers")),
        extract_message_text(post.get("followups")),
    ]

    return normalize_text(" ".join(parts))


def classify_topic(text: str) -> str:
    """Classify discussion using keyword matching."""
    text = text.lower()
    scores = {}

    for topic, keywords in TOPIC_KEYWORDS.items():
        scores[topic] = sum(
            1 for keyword in keywords
            if keyword in text
        )

    best_topic = max(scores, key=scores.get)

    if scores[best_topic] == 0:
        return "general"

    return best_topic


def classify_urgency(text: str) -> str:
    """Estimate urgency from discussion language."""
    text = text.lower()

    if any(word in text for word in URGENT_KEYWORDS):
        return "high"

    if any(word in text for word in MEDIUM_KEYWORDS):
        return "medium"

    return "low"


def classify_status(post: dict[str, Any]) -> str:
    """
    Determine status using explicit metadata.

    Avoid assuming a post is resolved simply
    because someone has answered it.
    """
    status = str(post.get("status") or "").lower()

    if status in {"resolved", "unresolved"}:
        return status

    if status in {"in_progress", "in progress"}:
        return "in_progress"

    if post.get("is_resolved") is True:
        return "resolved"

    if post.get("is_resolved") is False:
        return "unresolved"

    return "unknown"


def extract_keywords(
    text: str,
    limit: int = 5,
) -> list[str]:
    """Extract frequent meaningful words."""
    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z0-9_-]{2,}\b",
        text.lower(),
    )

    filtered = [
        word for word in words
        if word not in STOPWORDS
    ]

    counts = Counter(filtered)

    return [
        word for word, _ in counts.most_common(limit)
    ]


def generate_summary(
    post: dict[str, Any],
    max_length: int = 250,
) -> str:
    """
    Generate an extractive summary.

    This is a deterministic baseline, not
    a generative AI model.
    """
    title = normalize_text(
        str(post.get("title") or "")
    )

    content = normalize_text(
        str(post.get("content") or "")
    )

    if not content:
        return title[:max_length]

    sentences = re.split(
        r"(?<=[.!?])\s+",
        content,
    )

    first_sentence = sentences[0]

    summary = (
        f"{title}: {first_sentence}"
        if title
        else first_sentence
    )

    if len(summary) <= max_length:
        return summary

    return summary[:max_length - 3].rstrip() + "..."


def analyze_post(post: dict[str, Any]) -> dict[str, Any]:
    """
    Analyze one discussion and return
    structured information.
    """
    text = get_discussion_text(post)

    # Use the original question for topic and urgency
    # to avoid confusing answers with student intent.
    question_text = normalize_text(
        f"{post.get('title') or ''} "
        f"{post.get('content') or ''}"
    )

    return {
        "post_id": post.get("id"),
        "summary": generate_summary(post),
        "topic": classify_topic(question_text),
        "urgency": classify_urgency(question_text),
        "status": classify_status(post),
        "keywords": extract_keywords(text),
        "analysis_method": "keyword_baseline",
    }


def analyze_posts(
    posts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Analyze multiple discussions."""
    return [
        analyze_post(post)
        for post in posts
    ]
