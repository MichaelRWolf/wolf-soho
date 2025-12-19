# Git Workflow Instructions for Agent

## Git Commit Workflow

**When user requests "commit staged" or similar:**
1. ALWAYS check `git status` first to see what's already staged
2. ONLY run `git commit -m "message"` - DO NOT run `git add .`
3. Do not run `git push` after `git stage` unless explic `push` is explicitly requested.

**Key Distinctions:**
- "commit staged" = commit what's already staged (no `git add`)
- "commit all" = stage everything then commit (`git add .` then `git commit`)
- "stage and commit" = stage specific files then commit

**Common User Intentions:**
- "commit staged" = user has already staged files, just commit them
- "commit everything" = stage all changes then commit
- "commit X file" = stage specific file then commit

**Safety Check:**
Before committing, verify with `git status` that only intended files are staged.

## Example Workflow

**User says: "commit staged and push"**

**Correct sequence:**
```bash
git status          # Check what's staged
git commit -m "..." # Commit only staged files
git push            # Push the commit
```

**Incorrect sequence (what NOT to do):**
```bash
git add .           # DON'T do this unless explicitly requested
git commit -m "..." # This commits everything
git push
```

## Common Commands Reference

**Staging:**
- `git add <file>` - Stage specific file
- `git add .` - Stage all changes (use with caution)
- `git restore --staged <file>` - Unstage specific file

**Committing:**
- `git commit -m "message"` - Commit staged files only
- `git commit -am "message"` - Stage modified files and commit (skips untracked)

**Checking Status:**
- `git status` - See staged vs unstaged vs untracked files
- `git diff --staged` - See what's staged for commit
- `git diff` - See unstaged changes

## Best Practices

1. **Always check status first** - Know what you're committing
2. **Be explicit about staging** - Don't assume user wants everything staged
3. **Use descriptive commit messages** - Explain what changed and why
4. **Verify before pushing** - Make sure you're pushing the right commit
