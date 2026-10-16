# M-27 · Backup can't be written → nothing deleted

| | |
|---|---|
| **Part** | 6 · Forensics |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-16 11:25 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 1
- ✅ untracked file still there
- ✅ typed confirmation asked at the plan (the plan is above it)
- ✅ nothing asks again after the typed value
- ✅ the typed word is 'delete'
- ✅ screen says "Couldn't back up your files first, so nothing was deleted."
- ✅ …said once
- ✅ no absolute temp path on screen (the plan: a ~ path)
- ✅ no panic / raw error chain

## What a human should judge

After the typed word, refuses in one plain line, once: the backup couldn't be written, so nothing was deleted, and how to fix it (a ~ path, no error chain, F2); the file still exists.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
