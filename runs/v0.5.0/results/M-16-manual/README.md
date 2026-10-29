# M-16-manual · Undo → throw away: type to confirm, trash backup

| | |
|---|---|
| **Part** | 4 · Undo |
| **Model** | no |
| **Flagship** | ★ yes |
| **Run** | manual · 2026-10-29 10:50 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ commit gone
- ✅ working tree clean
- ✅ trash backup written
- ✅ screen shows 'backup'
- ✅ typed confirmation asked at the plan (the plan is above it)
- ✅ nothing asks again after the typed value
- ✅ Risks doesn't say the uncommitted work 'is gone' (F17)
- ✅ no panic / raw error chain

## What a human should judge

One confirmation (D1): the plan, its explanation, then the commit's SHA typed in place of Enter; the Risks text says uncommitted work is backed up, not gone; the success line names the backup.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings
