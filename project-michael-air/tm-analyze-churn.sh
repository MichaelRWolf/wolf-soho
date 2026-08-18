#!/usr/bin/env bash
# tm-analyze-churn.sh - Quick high-churn & contamination analysis for TM snapshots

set -euo pipefail

BACKUP_PATH="${1:-.}"

if [[ ! -d "$BACKUP_PATH" ]]; then
    echo "Error: Backup path does not exist: $BACKUP_PATH" >&2
    exit 1
fi

# Auto-detect the actual data path
if [[ "$BACKUP_PATH" == *".backup" ]] && [[ -d "$BACKUP_PATH/Macintosh HD - Data" ]]; then
    BACKUP_PATH="$BACKUP_PATH/Macintosh HD - Data"
elif [[ -d "$BACKUP_PATH/Macintosh HD - Data" ]]; then
    BACKUP_PATH="$BACKUP_PATH/Macintosh HD - Data"
fi

echo "=== Time Machine Snapshot Analysis ==="
echo "Backup: $BACKUP_PATH"
echo ""
echo "Format: BYTES_KB | HUMAN | PATH"
echo "---"
echo ""

# High-churn paths (should be 0) — from tm-cache-exclusions.md
declare -a CHURN=(
    # Package managers
    "opt/homebrew" ".cache/pip" ".cache/npm" ".cache/uv"
    ".cargo/registry/cache" ".gem/cache" "go/pkg/mod/cache"

    # IDEs & build tools
    "Library/Developer/Xcode/DerivedData" "Library/Developer/Xcode/Archives"
    "Library/Caches/Xcode" ".vscode/extensions" ".cache/JetBrains"
    ".cache/gradle" ".cache/maven"

    # System & app caches
    "Library/Caches" ".cache" ".cache/chromium" ".cache/fontconfig"

    # Language version managers
    ".local/share/uv/python" ".pyenv/versions" ".nvm" ".rbenv/versions"

    # Browser caches
    "Library/Application Support/Google/Chrome/Default/Cache"
    "Library/Application Support/Arc/User Data/Default/Cache"

    # Development tools
    ".cache/pre-commit" ".cache/huggingface" ".cache/torch"
)

# System paths (should be 0)
declare -a SYSTEM=(
    "System" "usr" "private" "opt" "var"
)

echo "## HIGH-CHURN PATHS (should be empty)"
for path in "${CHURN[@]}"; do
    full_path="$BACKUP_PATH/$path"
    if [[ -e "$full_path" ]]; then
        bytes=$(du -s "$full_path" 2>/dev/null | awk '{print $1}' | tr -d ' \n' || echo "0")
        bytes=${bytes:-0}
        human=$(numfmt --to=iec-i --suffix=B "$((bytes * 1024))" 2>/dev/null | sed 's/\([0-9.]\)\([KMGT]i*B\)$/\1 \2/' || printf "%d KB" "$bytes")
        printf "%10d | %9s | %s\n" "$bytes" "$human" "$path"
    fi
done
echo ""

echo "## SYSTEM FILES (⚠️ CONTAMINATION CHECK)"
total_system=0
has_system=0
for path in "${SYSTEM[@]}"; do
    full_path="$BACKUP_PATH/$path"
    if [[ -e "$full_path" ]]; then
        bytes=$(du -s "$full_path" 2>/dev/null | awk '{print $1}' | tr -d ' \n' || echo "0")
        bytes=${bytes:-0}
        human=$(numfmt --to=iec-i --suffix=B "$((bytes * 1024))" 2>/dev/null | sed 's/\([0-9.]\)\([KMGT]i*B\)$/\1 \2/' || printf "%d KB" "$bytes")
        if (( bytes > 0 )); then
            has_system=1
            total_system=$((total_system + bytes))
        fi
        printf "%10d | %9s | %s\n" "$bytes" "$human" "$path"
    fi
done
echo ""

# Verdict
if (( has_system == 1 )); then
    system_human=$(numfmt --to=iec-i --suffix=B "$((total_system * 1024))" 2>/dev/null | sed 's/\([0-9.]\)\([KMGT]i*B\)$/\1 \2/' || printf "%d KB" "$total_system")
    echo "❌ CONTAMINATION: $system_human of system files in backup"
    echo "   Recommendation: DELETE snapshot + apply cache exclusions + restart backup"
    echo ""
    exit 1
else
    echo "✓ CLEAN: No system file contamination"
    echo ""
    exit 0
fi
