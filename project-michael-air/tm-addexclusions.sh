#!/usr/bin/env bash
# tm-addexclusions.sh - Interactive TM exclusion manager with status display

set -euo pipefail

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'  # No Color

manage_exclusion() {
    local path="$1"

    # Skip if path doesn't exist
    if [[ ! -e "$path" ]]; then
        return
    fi

    # Get current status (tmutil output: "path: [Excluded]" or "path: [Included]")
    local status
    status=$(tmutil isexcluded "$path" 2>/dev/null | grep -oE '\[(Excluded|Included)\]' | tr -d '[]' || echo "Unknown")

    # Get size
    local size
    size=$(du -sh "$path" 2>/dev/null | awk '{print $1}' || echo "?")

    # Display current state, color path based on status
    local color
    case "$status" in
        Excluded) color="$RED" ;;      # Red: excluded from backup
        Included) color="$GREEN" ;;    # Green: included in backup
        *) color="$YELLOW" ;;          # Yellow: unknown/other
    esac

    printf "%-10s %8s  ${color}%s${NC}\n" "[$status]" "$size" "$path"

    # Prompt for action (default: Preserve)
    read -p "  [Preserve]/Toggle? (CR=Preserve): " -r response
    response="${response:-P}"  # Default to Preserve

    case "$response" in
        [Pp]|"")
            # Preserve - no action
            ;;
        [Tt])
            # Toggle
            case "$status" in
                Excluded)
                    echo "  Will run: tmutil removeexclusion '$path'"
                    read -p "  Confirm? y/N: " -r confirm
                    if [[ "$confirm" =~ ^[Yy]$ ]]; then
                        tmutil removeexclusion "$path"
                        echo "  ✓ Removed exclusion"
                    fi
                    ;;
                Included)
                    echo "  Will run: tmutil addexclusion -p '$path'"
                    read -p "  Confirm? y/N: " -r confirm
                    if [[ "$confirm" =~ ^[Yy]$ ]]; then
                        tmutil addexclusion -p "$path"
                        echo "  ✓ Added exclusion"
                    fi
                    ;;
                *)
                    echo "  (status unknown, cannot toggle)"
                    ;;
            esac
            ;;
        *)
            echo "  (invalid response)"
            ;;
    esac
    echo ""
}

declare -a EXCLUSIONS=(
    # Michael's favorites
    "/Applications"
    "$HOME/.cache"
    "$HOME/Downloads"
    "$HOME/Pictures"
    "$HOME/repos"

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
echo ""
echo "[Status]   Size     Path"
echo "─────────────────────────────────────────────────────────"
echo ""

for path in "${EXCLUSIONS[@]}"; do
    manage_exclusion "$path"
done

echo "Done."
