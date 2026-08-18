#!/usr/bin/env bash
# tm-addexclusions.sh - Interactive batch add Time Machine exclusions
# Prompts for each path, dry-run by just hitting CR on all prompts

set -euo pipefail

maybe_add_exclusion() {
    local path="$1"

    # Skip if path doesn't exist
    if [[ ! -e "$path" ]]; then
        return
    fi

    # Get size
    local size
    size=$(du -sh "$path" 2>/dev/null | awk '{print $1}' || echo "?")

    # Prompt user (default: NO)
    read -p "Add TM exclusion $path ($size)? y/N: " -r response
    response="${response:-N}"  # Default to N if empty (carriage return)

    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "  ✓ Adding: $path"
        tmutil addexclusion -p "$path"
    else
        echo "  (skip): $path"
    fi
}

declare -a EXCLUSIONS=(
    # Package managers
    "/opt/homebrew"
    "$HOME/.cache/pip"
    "$HOME/.cache/npm"
    "$HOME/.cache/uv"
    "$HOME/.cargo/registry/cache"
    "$HOME/.gem/cache"
    "$HOME/go/pkg/mod/cache"

    # IDEs & build tools
    "$HOME/Library/Developer/Xcode/DerivedData"
    "$HOME/Library/Developer/Xcode/Archives"
    "$HOME/Library/Caches/Xcode"
    "$HOME/.vscode/extensions"
    "$HOME/.cache/JetBrains"
    "$HOME/.cache/gradle"
    "$HOME/.cache/maven"

    # System & app caches
    "$HOME/Library/Caches"
    "$HOME/.cache"
    "$HOME/.cache/chromium"
    "$HOME/.cache/fontconfig"

    # Language version managers
    "$HOME/.local/share/uv/python"
    "$HOME/.pyenv/versions"
    "$HOME/.nvm"
    "$HOME/.rbenv/versions"

    # Browser caches
    "$HOME/Library/Application Support/Google/Chrome/Default/Cache"
    "$HOME/Library/Application Support/Arc/User Data/Default/Cache"

    # Development tools
    "$HOME/.cache/pre-commit"
    "$HOME/.cache/huggingface"
    "$HOME/.cache/torch"

    # System paths (high churn)
    "/private/var/db/diagnostics"
    "/private/var/db/Persist"
    "/private/var/log"
    "/private/tmp"
    "/private/var/tmp"

    # Application-specific
    "$HOME/Library/Application Support/Malwarebytes/MBAM/Db/Update/Installer"
)

echo "=== Time Machine Exclusion Manager ==="
echo "Tip: Just hit CR on all prompts for a dry-run (shows sizes, adds nothing)"
echo ""

added=0
skipped=0

for path in "${EXCLUSIONS[@]}"; do
    maybe_add_exclusion "$path"
    if [[ -e "$path" ]]; then
        if tmutil isexcluded "$path" 2>/dev/null | grep -q "Excluded"; then
            added=$((added + 1))
        else
            skipped=$((skipped + 1))
        fi
    fi
done

echo ""
echo "Summary: $added exclusions added, $skipped skipped"
