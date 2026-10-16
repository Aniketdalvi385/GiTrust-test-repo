# M-41 · Output piped into head doesn't crash

| | |
|---|---|
| **Part** | 8 · UX |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 11:25 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ no panic when the reader closes early
- ✅ …and it runs to completion: exit 0 (D5)

## What a human should judge

(checked by the runner with a closed pipe — see check). 'log' is an exact phrase, so no model is involved. v0.4.1's check (`… | head -1`) was a race: it caught the panic only when the reader left before the writes, so the reader now leaves first.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
