#!/usr/bin/env bash
# tm-addexclusions.sh - Batch add Time Machine exclusions
# Comment out any lines you don't want to exclude

# Package managers
tmutil addexclusion -p /opt/homebrew
tmutil addexclusion -p "$HOME/.cache/pip"
tmutil addexclusion -p "$HOME/.cache/npm"
tmutil addexclusion -p "$HOME/.cache/uv"
tmutil addexclusion -p "$HOME/.cargo/registry/cache"
tmutil addexclusion -p "$HOME/.gem/cache"
tmutil addexclusion -p "$HOME/go/pkg/mod/cache"

# IDEs & build tools
tmutil addexclusion -p "$HOME/Library/Developer/Xcode/DerivedData"
tmutil addexclusion -p "$HOME/Library/Developer/Xcode/Archives"
tmutil addexclusion -p "$HOME/Library/Caches/Xcode"
tmutil addexclusion -p "$HOME/.vscode/extensions"
tmutil addexclusion -p "$HOME/.cache/JetBrains"
tmutil addexclusion -p "$HOME/.cache/gradle"
tmutil addexclusion -p "$HOME/.cache/maven"

# System & app caches
tmutil addexclusion -p "$HOME/Library/Caches"
tmutil addexclusion -p "$HOME/.cache"
tmutil addexclusion -p "$HOME/.cache/chromium"
tmutil addexclusion -p "$HOME/.cache/fontconfig"

# Language version managers
tmutil addexclusion -p "$HOME/.local/share/uv/python"
tmutil addexclusion -p "$HOME/.pyenv/versions"
tmutil addexclusion -p "$HOME/.nvm"
tmutil addexclusion -p "$HOME/.rbenv/versions"

# Browser caches
tmutil addexclusion -p "$HOME/Library/Application Support/Google/Chrome/Default/Cache"
tmutil addexclusion -p "$HOME/Library/Application Support/Arc/User Data/Default/Cache"

# Development tools
tmutil addexclusion -p "$HOME/.cache/pre-commit"
tmutil addexclusion -p "$HOME/.cache/huggingface"
tmutil addexclusion -p "$HOME/.cache/torch"

# System paths (high churn)
tmutil addexclusion -p /private/var/db/diagnostics
tmutil addexclusion -p /private/var/db/Persist
tmutil addexclusion -p /private/var/log
tmutil addexclusion -p /private/tmp
tmutil addexclusion -p /private/var/tmp

# Application-specific
tmutil addexclusion -p "$HOME/Library/Application Support/Malwarebytes/MBAM/Db/Update/Installer"

echo "✓ All exclusions added"
