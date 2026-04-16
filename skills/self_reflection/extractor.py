"""Extract lessons and habit signals from sources."""
import re
from typing import List, Dict

from .adapter import ADAPTERS

def _extract_lessons(text: str) -> List[Dict]:
    """Return lessons with kind, text, and source hint."""
    lessons = []
    lines = text.split("\n")
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        lowered = stripped.lower()
        # Lessons typically written as bullet points or short statements
        # Detect patterns indicating a lesson/mistake/fix/rule
        if any(k in lowered for k in ["mistake", "wrong", "failed", "fix", "error", "bug", "missed", "remember", "avoid", "permanent"]):
            # Clean up trailing punctuation
            clean = stripped.rstrip(".")
            if "mistake" in lowered or "wrong" in lowered or "failed" in lowered or "missed" in lowered:
                kind = "mistake"
            elif "fix" in lowered or "fixed" in lowered or "added" in lowered or "changed" in lowered or "moved" in lowered:
                kind = "fix"
            elif "permanent" in lowered or "lesson" in lowered or "key takeaway" in lowered or "remember" in lowered:
                kind = "rule"
            else:
                kind = "insight"
            lessons.append({"kind": kind, "text": clean, "source": None})
    return lessons

def _extract_habits(text: str) -> List[Dict]:
    """Extract habit-related signals."""
    habits = []
    error_keywords = ["error", "failed", "bug", "fix", "missed", "broken", "timeout"]
    task_words = ["task", "job", "work", "todo", "issue"]
    lines = text.split("\n")
    error_count = sum(1 for line in lines if any(k in line.lower() for k in error_keywords))
    if error_count:
        habits.append({"type": "error_frequency", "value": error_count, "description": f"Found ~{error_count} error indicators"})
    task_count = sum(1 for line in lines if any(w in line.lower() for w in task_words))
    if task_count:
        habits.append({"type": "task_mention_frequency", "value": task_count, "description": f"Task mentions ~{task_count}"})
    return habits

def analyze() -> Dict:
    all_texts = []
    source_map = {}
    for name, reader in ADAPTERS.items():
        try:
            txt = reader()
            all_texts.append(txt)
            source_map[name] = txt[:200]
        except Exception:
            pass
    full = "\n\n".join(all_texts)
    lessons = _extract_lessons(full)
    habits = _extract_habits(full)
    return {
        "lessons": lessons,
        "habits": habits,
        "source_summary": {k: len(v) for k, v in source_map.items()},
    }