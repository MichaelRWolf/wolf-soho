#!/usr/bin/env bash
# analyze_linkedin_comments.sh
# Usage: ./analyze_linkedin_comments.sh parsed_comments_tagged_*.json

FILE="$1"

if [ -z "$FILE" ]; then
  echo "Usage: $0 <parsed_comments_tagged.json>"
  exit 1
fi

echo
echo "=== Total number of comments ==="
jq 'length' "$FILE"

echo
echo "=== Count of comments by posture ==="
jq '
  sort_by(.posture)
  | group_by(.posture)
  | map({ posture: .[0].posture, count: length })
  | sort_by(.count) | reverse
' "$FILE"

echo
echo "=== Unique assertions (with counts) ==="
jq '
  [ .[].assertions[] ]
  | group_by(.)
  | map({ assertion: .[0], count: length })
  | sort_by(.count) | reverse
' "$FILE"

echo
echo "=== Number of unique assertions ==="
jq '
  [ .[].assertions[] ]
  | unique
  | length
' "$FILE"

echo
echo "=== Assertions grouped by posture ==="
jq '
  sort_by(.posture)
  | group_by(.posture)
  | map({
      posture: .[0].posture,
      assertions: ([ .[].assertions[] ] | unique)
    })
' "$FILE"

echo
echo "=== Action-Offer comments (names only) ==="
jq -r '
  .[]
  | select(.posture == "Action-Offer")
  | "- " + .name
' "$FILE"
