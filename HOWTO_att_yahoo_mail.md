# ATT Yahoo Mail Login — Clean HOWTO

## Concept Overview

ATT email is a **federated login**:

- You start at a Yahoo-branded page
- You authenticate at **signin.att.com** (ATT identity provider)
- You land in **Yahoo Mail** (mail.yahoo.com)

The ugly URL is just OAuth/OIDC plumbing. Ignore it.

There are **two credential modes**:

1. **ATT password (normal)** → works in browsers
2. **Secure Mail Key (app password)** → required for Mail apps (iPhone/macOS Mail)

Goal: **one 1Password item + one Secure Mail Key** → works everywhere.

---

## (Full document continues exactly as in canvas…)
