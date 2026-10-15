# M-26 · Clean up: counts, untracked deleted, backed up

| | |
|---|---|
| **Part** | 6 · Forensics |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:41 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ junk/ deleted
- ✅ backup holds junk/inner/file.txt
- ✅ tracked edit untouched
- ✅ no panic / raw error chain

## What a human should judge

Gate shows how many files of each kind and names the backup. Note: deleting untracked files has no type-to-confirm (only the ⛔ plan + Enter) — the backup is their only copy.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
