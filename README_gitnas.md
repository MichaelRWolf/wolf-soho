# gitnas — NAS Git Remote Tools

Tools for managing git repos mirrored to `wolfden-nas`. All scripts live in
`wolf-soho/bin/` and are symlinked to `~/bin/` via `make install`.

---

## Family Tree

```text
gitnas-*
├── gitnas-repo-*          gh-derivatives (operate on repos)
│   ├── gitnas-repo-create
│   ├── gitnas-repo-setup
│   └── gitnas-repo-sync
└── gitnas-remote-*        git-derivative (operates on local git config)
    └── gitnas-remote-add
```

---

## Scripts

### `gitnas-repo-create` — lineage: `gh`

Creates a bare repo on the NAS. Equivalent to `gh repo create` but targets `wolfden-nas`
instead of GitHub.

```bash
# gh repo create (GitHub)
gh repo create MichaelRWolf/wolf-soho --private

# gitnas-repo-create (NAS equivalent)
ssh git-svc@wolfden-nas "git init --bare ~/git-repos/<name>.git"
```

Repo name and ownership sourced from `gh repo view` — no URL parsing.

---

### `gitnas-remote-add` — lineage: `git`

Adds `nas` as a remote to the local repo. Equivalent to `git remote add` but
pre-configured for the NAS URL pattern.

```bash
# git remote add (manual)
git remote add nas git-svc@wolfden-nas:git-repos/<name>.git

# gitnas-remote-add (pre-configured)
git remote add nas git-svc@wolfden-nas:git-repos/$(gh repo view --json name --jq '.name').git
```

Idempotent — exits cleanly if `nas` remote already exists.

---

### `gitnas-repo-setup` — lineage: `gh + git`

Combines `gitnas-repo-create` and `gitnas-remote-add`. The common case: one command
to set up a repo on NAS end-to-end.

```bash
gitnas-repo-create   # NAS side
gitnas-remote-add    # local side
```

---

### `gitnas-repo-sync` — lineage: `gh`

Pushes the current branch to the `nas` remote. Equivalent to `gh repo sync` but
pushes to NAS instead of syncing a GitHub fork.

```bash
# Single repo (current)
gitnas-repo-sync

# All repos under ~/repos/ that have a 'nas' remote
gitnas-repo-sync --all
```

---

## Hard-coded Configuration

All scripts share these constants (defined per-script as bash variables):

| Variable        | Value         | Purpose                      |
| --------------- | ------------- | ---------------------------- |
| `NAS_USER`      | `git-svc`     | SSH user on NAS              |
| `NAS_HOST`      | `wolfden-nas` | NAS hostname (in /etc/hosts) |
| `NAS_REPOS_DIR` | `git-repos`   | Bare repos directory on NAS  |
| `REMOTE_NAME`   | `nas`         | Local git remote name        |
