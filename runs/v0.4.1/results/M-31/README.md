# M-31 · Esc at a menu: calm cancel, exit 1, nothing done

| | |
|---|---|
| **Part** | 8 · UX |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:17 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 1
- ✅ screen shows 'Canceled — nothing was done.'
- ✅ HEAD untouched
- ✅ no panic / raw error chain

## What a human should judge

One calm line, no error styling.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: Esc at the undo menu cancels calmly, exit 1, HEAD untouched.

- Numbered 4-option menu ("[1–9 or ↑↓ + Enter to choose · Esc cancel]") with no Cancel row; help line mentions Esc.
- After Esc: "? Undo f4f7e88 ... <canceled>" then "↪  Canceled — nothing was done." Exit 1, HEAD unchanged.
- Some row descriptions are truncated with "…" (e.g. "unstag…", "you'll type to con…") at the test terminal width; cosmetic only.
