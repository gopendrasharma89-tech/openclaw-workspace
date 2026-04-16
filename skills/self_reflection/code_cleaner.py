"""Clean code/outputs to enforce pure, optimized style."""
import re
from pathlib import Path
from typing import Union

def remove_trailing_whitespace(content: str) -> str:
    lines = content.splitlines(keepends=True)
    cleaned = [re.sub(r"[ \t]+$", "", line) for line in lines]
    return "".join(cleaned)

def normalize_line_endings(content: str, style: str = "lf") -> str:
    # normalize to LF then ensure style
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    if style == "lf":
        return content
    elif style == "crlf":
        return content.replace("\n", "\r\n")
    return content

def remove_excess_blank_lines(content: str, max_consecutive: int = 2) -> str:
    lines = content.splitlines()
    out = []
    blank = 0
    for line in lines:
        if line.strip() == "":
            blank += 1
            if blank <= max_consecutive:
                out.append(line)
        else:
            blank = 0
            out.append(line)
    return "\n".join(out)

def strip_noop_comments(source: str) -> str:
    # Remove comment-only lines that are obviously noise (keep docstrings and meaningful comments)
    lines = source.splitlines()
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            # skip trivial comments that are just noise (heuristic)
            low = stripped.lower()
            if low.startswith("# ") and not any(word in low for word in ["todo", "fixme", "note", "important", "type:", "param:"]):
                continue
        cleaned.append(line)
    return "\n".join(cleaned)

def clean_code_file(path: Union[str, Path], dry_run: bool = False) -> dict:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    original = text
    text = remove_trailing_whitespace(text)
    text = strip_noop_comments(text)
    text = normalize_line_endings(text, "lf")
    text = remove_excess_blank_lines(text, max_consecutive=2)
    changed = text != original
    if changed and not dry_run:
        p.write_text(text, encoding="utf-8")
    return {"path": str(p), "changed": changed, "size_before": len(original), "size_after": len(text)}

def clean_directory(root: Union[str, Path], patterns=("*.py",), dry_run: bool = False):
    from glob import glob
    root = Path(root)
    results = []
    for pat in patterns:
        for f in root.rglob(pat):
            if f.is_file():
                results.append(clean_code_file(f, dry_run=dry_run))
    return results