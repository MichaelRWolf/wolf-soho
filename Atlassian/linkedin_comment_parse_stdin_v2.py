#!/usr/bin/env python3
"""
linkedin_comment_parse_stdin.py

Reads a LinkedIn comments scrape from STDIN and writes:
  - <STUB>_parsed_<timestamp>.json
  - <STUB>_parsed_<timestamp>.md

Usage:
  cat comments_scraped.txt | python3 linkedin_comment_parse_stdin.py comments
"""

import sys
import re
import json
import hashlib
import datetime as dt
from typing import List, Dict, Optional

# LinkedIn uses a few variants, e.g.:
#   "View Bryan Guffey’s open to work graphic link"
#   "View Kevin Mireles’  graphic link"
# We treat any line starting with "View " and containing "graphic link" as a segment starter.
VIEW_LINE_RE = re.compile(r"^View\s+.+graphic link\s*$")
TIME_RE = re.compile(r"\b(\d+)\s*(d|h|m)\b")

def collapse_blank_runs(lines: List[str]) -> List[str]:
    out: List[str] = []
    blank = False
    for l in lines:
        if l.strip() == "":
            if not blank:
                out.append("")
            blank = True
        else:
            out.append(l)
            blank = False
    return out

def segment_by_view_lines(lines: List[str]) -> List[List[str]]:
    starts: List[int] = []
    for i, l in enumerate(lines):
        if VIEW_LINE_RE.match(l.strip()):
            starts.append(i)
    starts.append(len(lines))
    return [lines[a:b] for a, b in zip(starts, starts[1:]) if lines[a:b]]

def looks_like_post_header(seg: List[str]) -> bool:
    head = "\n".join(seg[:60])
    return "Visible to anyone on or off LinkedIn" in head

def normalize_text(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{2,}", "\n", s)
    return s.strip()

def comment_id(identifier: str, text: str) -> str:
    base = identifier + "\n" + normalize_text(text)
    return hashlib.sha256(base.encode("utf-8")).hexdigest()[:16]

def extract_name_from_view_line(view_line: str) -> str:
    # Remove leading "View " and trailing "graphic link"
    s = view_line.strip()
    s = re.sub(r"^View\s+", "", s)
    s = re.sub(r"\s*graphic link\s*$", "", s).strip()

    # Remove common tail phrases (kept in identifier, removed from name)
    # e.g. "open to work"
    s = re.sub(r"\s+open to work\s*$", "", s).strip()

    # Strip possessive endings:
    #   "Bryan Guffey’s" -> "Bryan Guffey"
    #   "Kevin Mireles’" -> "Kevin Mireles"
    s = re.sub(r"[’']s\s*$", "", s).strip()
    s = re.sub(r"[’']\s*$", "", s).strip()

    return s

def extract_comment(seg: List[str]) -> Optional[Dict[str, str]]:
    view_line = seg[0].strip()
    if not VIEW_LINE_RE.match(view_line) or looks_like_post_header(seg):
        return None

    name = extract_name_from_view_line(view_line)
    start_idx = 1

    # Find a time-ish marker like "3d", "2d", etc, then start after it.
    for i, l in enumerate(seg[:80]):
        if TIME_RE.search(l):
            start_idx = i + 1
            break

    body: List[str] = []
    stop_tokens = {"like", "reply", "repost", "send", "report"}
    skip_exact = {"…more", "...more", "see translation"}

    for l in seg[start_idx:]:
        s = l.strip()
        if s == "":
            body.append("")
            continue
        if s.lower() in stop_tokens:
            break
        if s.lower() in skip_exact:
            continue
        # strip bare counters
        if re.fullmatch(r"\d+", s):
            continue
        body.append(s)

    body = collapse_blank_runs(body)
    text = "\n".join(body).strip()
    if not text:
        return None

    return {
        "name": name,
        "identifier": view_line,
        "text": text,
        "comment_id": comment_id(view_line, text),
    }

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
    if len(sys.argv) != 2:
        print("Usage: <stdin> | linkedin_comment_parse_stdin.py <stub>", file=sys.stderr)
        sys.exit(1)

    stub = sys.argv[1]
    raw = sys.stdin.read()
    lines = raw.splitlines()

    comments: List[Dict[str, str]] = []
    for seg in segment_by_view_lines(lines):
        c = extract_comment(seg)
        if c:
            comments.append(c)

    ts = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    json_path = f"{stub}_parsed_{ts}.json"
    md_path = f"{stub}_parsed_{ts}.md"

    with open(json_path, "w", encoding="utf-8") as jf:
        jf.write(json.dumps(comments, indent=2, ensure_ascii=False) + "\n")

    with open(md_path, "w", encoding="utf-8") as mf:
        mf.write(to_markdown(comments))

    print(f"[ok] wrote {json_path}")
    print(f"[ok] wrote {md_path}")

if __name__ == "__main__":
    main()
