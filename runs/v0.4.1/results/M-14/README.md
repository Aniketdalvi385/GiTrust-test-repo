# M-14 · Switching away would strand a commit → guard

| | |
|---|---|
| **Part** | 3 · Stuck states |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:17 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ the detached commit is on a branch
- ✅ no panic / raw error chain

## What a human should judge

Says the commit would be stranded and offers a branch first; nothing lost.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
