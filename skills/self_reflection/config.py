"""Configuration for the Self-Reflection & Habit Tracker."""
import os
from pathlib import Path

BASE = Path(__file__).parent

SOURCE_ADAPTERS = [
    "memory",
    "daily_notes",
    "heartbeat",
    "git_log",
    "task_queue",
]

HABIT_STATE_PATH = BASE.parent.parent.parent / "habits" / "tracker.json"

# Cleaning behavior
CLEAN_MAX_CONSECUTIVE_BLANK_LINES = 2
CLEAN_STRICT_COMMENTS = False  # if True, drop more comments