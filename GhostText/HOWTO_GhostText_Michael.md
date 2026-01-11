# HOWTO: GhostText Setup (Michael Edition)

This guide is **setup only**.

Assumptions:
- Apple Silicon Mac
- Homebrew installed
- No interest in dead ends

Goal:
> **Chrome + GhostText + native VS Code = durable, crash-proof 2-way sync**

---

## Step 1 — Install VS Code (native)

```bash
brew install --cask visual-studio-code
```

Launch once:
```bash
open -a "Visual Studio Code"
```

---

## Step 2 — Verify native Apple Silicon

Activity Monitor → Visual Studio Code → **Kind = Apple**

If not, stop and fix before continuing.

---

## Step 3 — Install GhostText in VS Code

- Open VS Code
- Extensions (⇧⌘X)
- Install **GhostText for VS Code**

---

## Step 4 — Install GhostText in Chrome

- Chrome Web Store
- Install **GhostText**
- Pin the 👻 icon

---

## Step 5 — Create workspace

```bash
mkdir -p ~/WebForms
```

VS Code:
- File → Open Folder… → `~/WebForms`

---

## Step 6 — Restore workspace on launch

Ensure:
```
window.restoreWindows = all
```

Open WebForms once, quit VS Code normally.

---

## Step 7 — Add VS Code to Login Items

System Settings → General → Login Items → Add:
```
/Applications/Visual Studio Code.app
```

---

## Step 8 — Test

1. Open Chrome
2. Open a page with a text field
3. Click inside field
4. Click 👻 GhostText
5. Choose VS Code

Confirm live 2-way sync.

---

## Done

You now have:
- Native VS Code
- GhostText live sync
- Crash protection
- Optional file snapshots
