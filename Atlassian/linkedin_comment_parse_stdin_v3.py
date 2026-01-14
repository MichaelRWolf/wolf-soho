#!/usr/bin/env python3
"""
linkedin_comment_parse_stdin.py (v3)

Reads a LinkedIn post-page scrape from STDIN and extracts *comments* (not reactions),
writing:
  - <STUB>_parsed_<timestamp>.json
  - <STUB>_parsed_<timestamp>.md

Usage:
  cat comments_scraped.txt | python3 linkedin_comment_parse_stdin_v3.py comments

Notes:
- This version ignores the "Reactions" avatar list by requiring a time marker (e.g. 3d, 2h).
"""

import sys
import re
import json
import hashlib
import datetime as dt
from typing import List, Dict, Optional, Tuple

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
    head = "\n".join(seg[:80])
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
    s = view_line.strip()
    s = re.sub(r"^View\s+", "", s)
    s = re.sub(r"\s*graphic link\s*$", "", s).strip()
    s = re.sub(r"\s+open to work\s*$", "", s).strip()
    s = re.sub(r"[’']s\s*$", "", s).strip()
    s = re.sub(r"[’']\s*$", "", s).strip()
    return s

def find_time_index(seg: List[str], max_scan: int = 120) -> Optional[int]:
    # Find a line that contains time like "3d" or "2h".
    for i, l in enumerate(seg[:max_scan]):
        if TIME_RE.search(l):
            return i
    return None

def extract_comment(seg: List[str]) -> Optional[Dict[str, str]]:
    view_line = seg[0].strip()
    if not VIEW_LINE_RE.match(view_line) or looks_like_post_header(seg):
        return None

    time_i = find_time_index(seg)
    # Critical fix: Reactions list entries have no time marker, so ignore them.
    if time_i is None:
        return None

    name = extract_name_from_view_line(view_line)
    start_idx = time_i + 1

    body: List[str] = []
    stop_tokens = {"like", "reply", "repost", "send", "report", "collapse replies"}
    skip_exact = {"…more", "...more", "see translation", "show translation"}

    for l in seg[start_idx:]:
        s = l.strip()
        if s == "":
            body.append("")
            continue
        sl = s.lower()
        if sl in stop_tokens:
            break
        if sl in skip_exact:
            continue
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
        print("Usage: <stdin> | linkedin_comment_parse_stdin_v3.py <stub>", file=sys.stderr)
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
    print(f"[ok] extracted {len(comments)} comments")

if __name__ == "__main__":
    main()
