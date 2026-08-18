#!/usr/bin/env bash
# tm-addexclusions.sh - Batch add Time Machine exclusions
# Only adds exclusions for paths that exist

set -euo pipefail

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

echo "Adding Time Machine exclusions..."
echo ""

added=0
skipped=0

for path in "${EXCLUSIONS[@]}"; do
    if [[ -e "$path" ]]; then
        echo "✓ Adding: $path"
        tmutil addexclusion -p "$path"
        added=$((added + 1))
    else
        echo "  (skip, doesn't exist yet): $path"
        skipped=$((skipped + 1))
    fi
done

echo ""
echo "Summary: $added exclusions added, $skipped skipped (path doesn't exist)"
