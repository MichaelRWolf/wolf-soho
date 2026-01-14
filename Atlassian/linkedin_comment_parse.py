#!/usr/bin/env python3
"""
linkedin_comment_parse.py

Parse a "Cmd-A / Cmd-C" full-page LinkedIn post scrape (plain text) into
separated comment blocks in Markdown (and optional JSON).

Design goals:
- One-time extraction for analysis/summarization
- Ignore nesting (replies vs. top-level)
- Robust-ish against LinkedIn UI noise included in the paste

Usage:
  python3 linkedin_comment_parse.py posting_scraped.txt > comments.md
  python3 linkedin_comment_parse.py posting_scraped.txt --json comments.json
"""

from __future__ import annotations

import argparse
import itertools
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


START_RE = re.compile(r"^View (.+?)[’']s .*graphic link$")
TIME_RE = re.compile(r"\b(\d+)\s*(d|h|m)\b")
REACTION_WORDS = {"like", "funny", "support", "insightful", "celebrate", "love"}


def _collapse_blank_runs(lines: List[str]) -> List[str]:
    out: List[str] = []
    for is_blank, grp in itertools.groupby(lines, key=lambda x: x.strip() == ""):
        if is_blank:
            out.append("")
        else:
            out.extend(list(grp))
    # trim leading/trailing blanks
    while out and out[0] == "":
        out = out[1:]
    while out and out[-1] == "":
        out = out[:-1]
    return out


def _segment_by_view_lines(lines: List[str]) -> List[List[str]]:
    """Split the full scrape into segments that start with 'View <Name>’s ... graphic link'."""
    starts: List[int] = []
    for i, l in enumerate(lines):
        if l.startswith("View ") and "graphic link" in l:
            starts.append(i)
    starts.append(len(lines))

    segs: List[List[str]] = []
    for a, b in zip(starts, starts[1:]):
        seg = lines[a:b]
        if seg:
            segs.append(seg)
    return segs


def _looks_like_post_header(seg: List[str]) -> bool:
    head = "\n".join(seg[:40])
    # The author/post header tends to include this visibility line.
    return "Visible to anyone on or off LinkedIn" in head


def _extract_comment(seg: List[str]) -> Optional[Dict[str, str]]:
    view_line = seg[0].strip()
    m = START_RE.match(view_line)
    if not m:
        return None

    name = m.group(1).strip()

    if _looks_like_post_header(seg):
        return None  # skip the main post itself

    # Find a "time-ish" line, then start body after the first blank line after it.
    start_idx = 1
    time_idx: Optional[int] = None
    for i, l in enumerate(seg[:80]):
        if TIME_RE.search(l) and ("ago" in l or "•" in l or l.strip().endswith(("d", "h", "m"))):
            time_idx = i
            break

    if time_idx is not None:
        for j in range(time_idx + 1, min(len(seg), time_idx + 40)):
            if seg[j].strip() == "":
                start_idx = j + 1
                break
        else:
            start_idx = time_idx + 1

    body_lines: List[str] = []
    for l in seg[start_idx:]:
        s = l.strip()

        if s == "":
            body_lines.append("")
            continue

        # Stop on obvious UI action labels.
        if s.lower() in {"like", "reply", "repost", "send", "report"}:
            break

        # Drop common UI noise (keep this conservative; we don't want to delete real content).
        if s in {"…more", "...more"}:
            continue
        if s.lower() in {"reactions", "see translation", "edited"}:
            continue

        # Drop standalone counters that typically trail UI sections (best-effort).
        if re.fullmatch(r"\d+", s):
            continue
        if re.fullmatch(r"\d+\s+comments?", s.lower()):
            break
        if re.fullmatch(r"\d+\s+reposts?", s.lower()):
            break

        body_lines.append(s)

    body_lines = _collapse_blank_runs(body_lines)
    body = "\n".join(body_lines).strip()

    # Filter out reaction-only segments (these often appear near the top as 'like', 'funny', etc.)
    if body.lower() in REACTION_WORDS and len(body.split()) == 1:
        return None

    if not body:
        return None

    return {"name": name, "identifier": view_line, "text": body}


def parse_file(path: Path) -> List[Dict[str, str]]:
    raw = path.read_text(errors="ignore")
    lines = raw.splitlines()
    segments = _segment_by_view_lines(lines)

    comments: List[Dict[str, str]] = []
    for seg in segments:
        c = _extract_comment(seg)
        if c:
            comments.append(c)
    return comments


def to_markdown(comments: List[Dict[str, str]]) -> str:
    out: List[str] = []
    for c in comments:
        out.append(f"## {c['name']}")
        out.append(c["identifier"])
        out.append("")
        out.append(c["text"])
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="Path to the plain-text LinkedIn page scrape")
    ap.add_argument("--json", dest="json_path", help="Optional: write parsed comments to JSON")
    args = ap.parse_args()

    comments = parse_file(Path(args.input))

    if args.json_path:
        Path(args.json_path).write_text(json.dumps(comments, indent=2, ensure_ascii=False) + "\n")

    print(to_markdown(comments), end="")


if __name__ == "__main__":
    main()
