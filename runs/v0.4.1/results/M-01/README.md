# M-01 · Exact phrase works with the model down

| | |
|---|---|
| **Part** | 1 · Everyday |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:16 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ screen shows 'Show status'
- ✅ screen never shows "isn't running"
- ✅ status says how old the remote view is
- ✅ no panic / raw error chain

## What a human should judge

Instant; ⚡ line; no complaint about the model.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: Instant status with the model down, no model complaint.

- First line "⚡  Show status", exit 0, 0.0s, no mention of the model.
- Status ends with "Remote state as of the last fetch, just now — gitrust "fetch" refreshes it." which is clear and useful.
