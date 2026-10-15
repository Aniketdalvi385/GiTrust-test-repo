# M-35 · Learned phrase: a menu pick is instant next time

| | |
|---|---|
| **Part** | 8 · UX |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:17 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ screen shows 'learned'
- ✅ learned run exits 0
- ✅ screen shows 'whats goin on'
- ✅ forget exits 0
- ✅ no panic / raw error chain

## What a human should judge

Second run says '· learned' and works with the model down; `aliases` lists it.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
