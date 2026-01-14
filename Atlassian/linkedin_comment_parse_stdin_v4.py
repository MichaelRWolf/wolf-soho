#!/usr/bin/env python3
"""
linkedin_comment_parse_stdin_v4.py

Reads a LinkedIn post-page scrape from STDIN and extracts comments (not reactions),
writing:
  - <STUB>_parsed_<timestamp>.json
  - <STUB>_parsed_<timestamp>.md

Also emits WARNINGS (to stderr) if the scrape appears incomplete:
  - hidden sub-comments (e.g. "See 3 more replies", "See previous replies")
  - truncated comment text (e.g. "…more" / "...more")

Usage:
  cat comments_scraped.txt | python3 linkedin_comment_parse_stdin_v4.py comments
  head -n 150 comments_scraped.txt | python3 linkedin_comment_parse_stdin_v4.py comments

Tip:
  Expand all "...more" and expand all replies in the browser before scraping
  if you want complete capture.
"""

import sys
import re
import json
import hashlib
import datetime as dt
from typing import List, Dict, Optional

VIEW_LINE_RE = re.compile(r"^View\s+.+graphic link\s*$")
TIME_RE = re.compile(r"\b(\d+)\s*(d|h|m)\b")

# Incomplete-scrape indicators
TRUNC_MORE_RE = re.compile(r"^(…more|\.\.\.more)$", re.IGNORECASE)
HIDDEN_REPLIES_RE = re.compile(r"^See\s+(\d+)\s+more\s+repl(ies|y)\b", re.IGNORECASE)
SEE_PREVIOUS_REPLIES_RE = re.compile(r"^See\s+previous\s+repl(ies|y)\b", re.IGNORECASE)

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

def find_time_index(seg: List[str], max_scan: int = 140) -> Optional[int]:
    for i, l in enumerate(seg[:max_scan]):
        if TIME_RE.search(l):
            return i
    return None

def scan_incomplete_markers(seg: List[str]) -> Dict[str, object]:
    trunc = 0
    hidden_more_replies = 0
    see_prev_replies = 0
    hidden_reply_counts: List[int] = []

    for l in seg:
        s = l.strip()
        if TRUNC_MORE_RE.match(s):
            trunc += 1
        m = HIDDEN_REPLIES_RE.match(s)
        if m:
            hidden_more_replies += 1
            try:
                hidden_reply_counts.append(int(m.group(1)))
            except Exception:
                pass
        if SEE_PREVIOUS_REPLIES_RE.match(s):
            see_prev_replies += 1

    return {
        "has_truncated_more": trunc > 0,
        "truncated_more_count": trunc,
        "has_hidden_more_replies": hidden_more_replies > 0,
        "hidden_more_replies_markers": hidden_more_replies,
        "hidden_reply_counts": hidden_reply_counts,
        "has_see_previous_replies": see_prev_replies > 0,
        "see_previous_replies_markers": see_prev_replies,
    }

def extract_comment(seg: List[str]) -> Optional[Dict[str, object]]:
    view_line = seg[0].strip()
    if not VIEW_LINE_RE.match(view_line) or looks_like_post_header(seg):
        return None

    time_i = find_time_index(seg)
    # Reaction avatar list entries typically have no "3d/2h" line; ignore them.
    if time_i is None:
        return None

    name = extract_name_from_view_line(view_line)
    markers = scan_incomplete_markers(seg)

    start_idx = time_i + 1
    body: List[str] = []
    stop_tokens = {"like", "reply", "repost", "send", "report", "collapse replies"}
    skip_exact = {"see translation", "show translation"}

    for l in seg[start_idx:]:
        s = l.strip()
        if s == "":
            body.append("")
            continue

        sl = s.lower()
        if sl in stop_tokens:
            break

        # Keep indicators out of comment text, but we already recorded them via markers.
        if TRUNC_MORE_RE.match(s):
            continue
        if HIDDEN_REPLIES_RE.match(s) or SEE_PREVIOUS_REPLIES_RE.match(s):
            continue

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
        "flags": {
            "comment_text_truncated": bool(markers["has_truncated_more"]),
            "hidden_subcomments_present": bool(markers["has_hidden_more_replies"] or markers["has_see_previous_replies"]),
            "hidden_reply_counts": markers["hidden_reply_counts"],
            "see_previous_replies_markers": markers["see_previous_replies_markers"],
        },
    }

def to_markdown(comments: List[Dict[str, object]]) -> str:
    out: List[str] = []
    for c in comments:
        out.append(f"## {c['name']}")
        out.append(str(c["identifier"]))
        out.append("")
        flags = c.get("flags", {}) or {}
        notes: List[str] = []
        if flags.get("comment_text_truncated"):
            notes.append("⚠️ comment text truncated (…more)")
        if flags.get("hidden_subcomments_present"):
            notes.append("⚠️ hidden sub-comments (replies not fully expanded)")
        if notes:
            out.append("_" + "; ".join(notes) + "_")
            out.append("")
        out.append(str(c["text"]))
        out.append("")
    return "\n".join(out).rstrip() + "\n"

def warn_incomplete(comments: List[Dict[str, object]]) -> None:
    trunc = sum(1 for c in comments if (c.get("flags") or {}).get("comment_text_truncated"))
    hidden = sum(1 for c in comments if (c.get("flags") or {}).get("hidden_subcomments_present"))

    if trunc:
        print(f"[warn] {trunc} comment(s) appear truncated (…more). Expand all '…more' before scraping for complete text.", file=sys.stderr)
    if hidden:
        print(f"[warn] {hidden} comment(s) indicate hidden sub-comments (replies not fully expanded). Expand all replies before scraping for complete capture.", file=sys.stderr)

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: <stdin> | linkedin_comment_parse_stdin_v4.py <stub>", file=sys.stderr)
        sys.exit(1)

    stub = sys.argv[1]
    raw = sys.stdin.read()
    lines = raw.splitlines()

    comments: List[Dict[str, object]] = []
    for seg in segment_by_view_lines(lines):
        c = extract_comment(seg)
        if c:
            comments.append(c)

    warn_incomplete(comments)

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
