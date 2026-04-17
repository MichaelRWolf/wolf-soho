# Identity Strategy -- NAS + Mac -- Human and Service Accounts

## Account Classification

| Type    | Definition                              | Examples            |
| ------- | --------------------------------------- | ------------------- |
| Human   | Interactive login + personal storage    | michael, wendy      |
| Service | Automated role only, no interactive use | tm-michael-pro, git |

---

## Human Accounts

### Current state

| System | Username     |
| ------ | ------------ |
| Mac    | michael      |
| Mac    | wendy        |
| NAS    | michaelrwolf |
| NAS    | wendyrwolf   |

### Recommended long-term: unify across all systems

```text
michael  -- everywhere (Mac + NAS)
wendy    -- everywhere (Mac + NAS)
```

**Benefits:**

- SSH between Macs and NAS feels SSO-like
- File ownership matches across systems
- No mental translation layer (`michael` vs `michaelrwolf`)
- Muscle memory stays simple

---

## Service Accounts

Service accounts have automated roles only. No interactive shell use, no personal
storage. Auth via SSH key; password login disabled.

### Pattern: TimeMachine

```text
tm-<hostname>
```

One account per backup client machine. Machine-scoped so DSM can show per-device
quota and backup status.

Examples:

- `tm-michael-pro`
- `tm-wolf-air`

### Pattern: Git service

```text
git
```

NAS-scoped (single instance -- the NAS hosts git repos, one account serves all).
No machine suffix needed.

**Why `git` is a safe name despite being guessable:**

- Auth is SSH key only -- no password to guess
- Password login disabled for this account
- `git` is the Unix/GitHub convention (`git@github.com` uses the same pattern)
- Guessable username is irrelevant when password auth is off

**Synology setup:**

- User `git` created in DSM (no admin, no app services)
- SSH public key uploaded in DSM user settings
- Bare repos live in `git-repos/` shared folder (Read/Write for `git` user)
- URL format: `git@wolfden-nas:git-repos/FY-2024.git` (relative to `git` user home)
- No `/volume1` in URLs -- internal path is an implementation detail

---

## Summary Table

| Account        | Type    | Scope         | Auth     | Purpose                     |
| -------------- | ------- | ------------- | -------- | --------------------------- |
| michael        | Human   | Mac + NAS     | password | Interactive, personal files |
| wendy          | Human   | Mac + NAS     | password | Interactive, personal files |
| tm-michael-pro | Service | NAS (per Mac) | SSH key  | TimeMachine backup          |
| tm-wolf-air    | Service | NAS (per Mac) | SSH key  | TimeMachine backup          |
| git            | Service | NAS           | SSH key  | Git bare repo hosting       |
