"""Adapters for reading sources used by the Self-Reflection & Habit Tracker."""
import os
import re
from pathlib import Path

from .config import SOURCE_ADAPTERS, HABIT_STATE_PATH

def read_root(path_suffix):
    # resolve relative to repo root (two possible locations)
    for base in [Path(__file__).parent.parent.parent.parent, Path.cwd()]:
        p = base / path_suffix
        if p.exists():
            return p
    return None

def read_memory():
    p = read_root("MEMORY.md")
    return p.read_text(encoding="utf-8") if p else ""

def read_daily_notes():
    notes_dir = Path(__file__).parent.parent.parent.parent / "memory"
    texts = []
    for f in sorted(notes_dir.glob("*.md")):
        texts.append(f.read_text(encoding="utf-8"))
    return "\n".join(texts)

def read_heartbeat():
    p = Path(__file__).parent.parent.parent.parent / "HEARTBEAT.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""

def read_git_log(limit=20):
    import subprocess
    repo_root = Path(__file__).parent.parent.parent.parent
    cmd = ["git", "log", "--oneline", f"-{limit}"]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_root)
    return result.stdout

def read_task_queue():
    f = Path(__file__).parent.parent.parent.parent / "tasks" / "QUEUE.md"
    return f.read_text(encoding="utf-8") if f.exists() else ""

ADAPTERS = {
    "memory": read_memory,
    "daily_notes": read_daily_notes,
    "heartbeat": read_heartbeat,
    "git_log": read_git_log,
    "task_queue": read_task_queue,
}

def read_source(name: str):
    if name in ADAPTERS:
        return ADAPTERS[name]()
    raise ValueError(f"Unknown source: {name}")