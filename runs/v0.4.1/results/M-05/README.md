# M-05 · Create a branch; dirty switch is handled

| | |
|---|---|
| **Part** | 1 · Everyday |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 18:01 |
| **Automatic checks** | ❌ failed |

## Checks

- ✅ branch created (exit 0)
- ✅ feature-x exists
- ✅ the uncommitted edit survives the switch attempt
- ✅ a refused switch does not exit 0
- ✅ no panic / raw error chain
- ❌ no panic / raw error chain — `caused by:`

## What a human should judge

Branch created; switching back with uncommitted edits either works safely or is refused with a clear reason — never a crash, never lost edits.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
