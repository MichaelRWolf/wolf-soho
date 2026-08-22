#!/usr/bin/env bash
# Intel x86_64 binary audit for wendy-air
# Adapted from michael-air audit (2026-08-15)
# See github.com/MichaelRWolf/wolf-soho/issues/8

exec > x86_64-audit.log 2>&1

echo "=== Intel x86_64 Audit for wendy-air ==="
echo "Started: $(date)"
echo

echo "## 1. Common package locations"
echo "### /usr/local binaries"
find /usr/local -type f -executable -print0 2>/dev/null | xargs -0 file 2>/dev/null | grep x86_64 | head -50

echo
echo "### /opt binaries"
find /opt -type f -executable -print0 2>/dev/null | xargs -0 file 2>/dev/null | grep x86_64 | head -50

echo
echo "### ~/.local binaries"
find ~/.local -type f -executable -print0 2>/dev/null | xargs -0 file 2>/dev/null | grep x86_64 | head -50

echo
echo "## 2. Interpreters and shells"
for cmd in python3 python ruby node ruby npm perl; do
  if which $cmd &>/dev/null; then
    echo "### $(which $cmd)"
    file "$(which $cmd)"
  fi
done

echo
echo "## 3. PATH audit"
echo "Current PATH:"
echo "$PATH" | tr ':' '\n' | nl
echo
echo "### x86_64 binaries in PATH:"
echo "$PATH" | tr ':' '\n' | while read -r dir; do
  [ -d "$dir" ] && file "$dir"/* 2>/dev/null | grep x86_64 | sed "s|^|$dir/|" || true
done

echo
echo "## 4. Python site-packages"
python_paths=$(python3 -c "import site; print('\n'.join(site.getsitepackages() + [site.getusersitepackages()]))" 2>/dev/null)
if [ -n "$python_paths" ]; then
  echo "$python_paths" | while read -r path; do
    if [ -d "$path" ]; then
      echo "### $path"
      find "$path" \( -name "*.so" -o -name "*.pyd" \) -print0 2>/dev/null | xargs -0 file 2>/dev/null | grep x86_64 | head -10 || echo "  (no x86_64 extensions)"
    fi
  done
fi

echo
echo "## 5. Ruby gems"
if which gem &>/dev/null; then
  echo "### Checking gem native extensions"
  find ~/.gem -name "*.so" -print0 2>/dev/null | xargs -0 file 2>/dev/null | grep x86_64 | head -10 || echo "  (no x86_64 gems)"
fi

echo
echo "## 6. /Applications bundles"
echo "### Scanning /Applications for x86_64 binaries (first 30)"
find /Applications -type f -executable -print0 2>/dev/null | xargs -0 file 2>/dev/null | grep x86_64 | head -30

echo
echo "## 7. System LaunchAgents/LaunchDaemons"
echo "### Checking for x86_64 in launch items"
sudo find /Library/LaunchAgents /Library/LaunchDaemons ~/Library/LaunchAgents ~/Library/LaunchDaemons -type f 2>/dev/null | xargs file 2>/dev/null | grep x86_64 | head -20 || echo "  (none found or permission denied)"

echo
echo "## 8. Xcode derived data"
if [ -d ~/Library/Developer/Xcode/DerivedData ]; then
  echo "### Checking Xcode DerivedData for x86_64 builds"
  find ~/Library/Developer/Xcode/DerivedData -type f -executable -print0 2>/dev/null | xargs -0 file 2>/dev/null | grep x86_64 | head -10 || echo "  (none found)"
fi

echo
echo "## 9. npm/node_modules"
if [ -d ~/.npm ]; then
  echo "### Checking ~/.npm for native modules"
  find ~/.npm -name "*.node" -print0 2>/dev/null | xargs -0 file 2>/dev/null | grep x86_64 | head -10 || echo "  (none found)"
fi

echo
echo "=== Audit Complete ==="
echo "Finished: $(date)"
