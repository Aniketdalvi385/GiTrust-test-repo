# M-31 · Esc at a menu: calm cancel, exit 1, nothing done

| | |
|---|---|
| **Part** | 8 · UX |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 11:25 |
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
