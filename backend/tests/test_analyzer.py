
from app.services.analyzer import (
    analyze_post,
    classify_topic,
    classify_urgency,
    classify_status,
)


def test_assignment_classification():
    text = "When is the homework assignment due?"

    assert classify_topic(text) == "assignments"


def test_high_urgency():
    text = "Urgent! I cannot submit my assignment."

    assert classify_urgency(text) == "high"


def test_low_urgency():
    text = "Can someone explain this concept?"

    assert classify_urgency(text) == "low"


def test_resolved_status():
    post = {
        "status": "resolved",
        "is_resolved": True,
    }

    assert classify_status(post) == "resolved"


def test_answer_does_not_imply_resolution():
    post = {
        "answers": [
            {"content": "Try changing your code."}
        ]
    }

    assert classify_status(post) == "unknown"


def test_analyze_post():
    post = {
        "id": "test_001",
        "title": "Homework submission error",
        "content": "Urgent! I cannot submit my homework.",
        "status": "unresolved",
        "answers": [],
        "followups": [],
    }

    result = analyze_post(post)

    assert result["post_id"] == "test_001"
    assert result["topic"] == "assignments"
    assert result["urgency"] == "high"
    assert result["status"] == "unresolved"
    assert result["analysis_method"] == "keyword_baseline"
