"""Maintain habit state and produce suggestions."""
import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List

from .config import HABIT_STATE_PATH

def _default_state() -> Dict[str, Any]:
    return {
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "sessionCount": 0,
        "totalLessons": 0,
        "mistakeCount": 0,
        "fixCount": 0,
        "ruleCount": 0,
        "lastLessons": [],
        "recentErrors": [],
        "suggestions": [],
    }

def load_state() -> Dict[str, Any]:
    path = HABIT_STATE_PATH
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            # ensure keys exist
            for k in _default_state().keys():
                data.setdefault(k, _default_state()[k] if k != "lastLessons" else [])
            return data
        except Exception:
            pass
    return _default_state()

def save_state(state: Dict[str, Any]):
    state["updatedAt"] = datetime.now(timezone.utc).isoformat()
    state["sessionCount"] += 1
    p = HABIT_STATE_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def ingest_analysis(analysis: Dict):
    state = load_state()
    lessons: List[Dict] = analysis.get("lessons", [])
    habits: List[Dict] = analysis.get("habits", [])
    # update totals
    state["totalLessons"] += len(lessons)
    for l in lessons:
        if l["kind"] == "mistake":
            state["mistakeCount"] += 1
        elif l["kind"] == "fix":
            state["fixCount"] += 1
        elif l["kind"] == "rule":
            state["ruleCount"] += 1
        state["lastLessons"].insert(0, {"text": l["text"], "kind": l["kind"], "at": datetime.now(timezone.utc).isoformat()})
    # keep only last 20
    state["lastLessons"] = state["lastLessons"][:20]
    # extract recent errors
    for h in habits:
        if h["type"] == "error_frequency":
            state["recentErrors"].append({"description": h["description"], "at": datetime.now(timezone.utc).isoformat()})
    # produce simple suggestions if mistakes persist
    if state["mistakeCount"] > state["fixCount"] + 2:
        state["suggestions"].append("Focus on writing tests before code to prevent repeated mistakes.")
    if len(state["recentErrors"]) > 5:
        state["suggestions"].append("Review and refactor recent error-prone modules.")
    save_state(state)
    return state

def get_suggestions(limit=5) -> List[str]:
    state = load_state()
    return state.get("suggestions", [])[:limit]