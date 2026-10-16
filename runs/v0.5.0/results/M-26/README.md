# M-26 · Clean up: counts, untracked deleted, backed up

| | |
|---|---|
| **Part** | 6 · Forensics |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 11:25 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ junk/ deleted
- ✅ backup holds junk/inner/file.txt
- ✅ tracked edit untouched
- ✅ typed confirmation asked at the plan (the plan is above it)
- ✅ nothing asks again after the typed value
- ✅ the typed word is 'delete'
- ✅ the backup line doesn't call them 'discarded changes' (F17)
- ✅ no raw git output 'Successfully rebased'
- ✅ no raw git output 'Enumerating objects'
- ✅ no raw git output 'Removing'
- ✅ no panic / raw error chain

## What a human should judge

Gate shows how many files of each kind and names the backup. Deleting untracked files needs a typed word at the plan, like a hard reset (D2) — the backup is their only copy; the success line calls them deleted files, not discarded changes.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
