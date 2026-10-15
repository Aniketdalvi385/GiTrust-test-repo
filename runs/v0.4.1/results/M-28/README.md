# M-28 · --recover with nothing to recover points to forensics

| | |
|---|---|
| **Part** | 6 · Forensics |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:39 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ screen shows 'find my lost work'
- ✅ no panic / raw error chain

## What a human should judge

Says there's nothing interrupted and suggests 'find my lost work'.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: Says nothing interrupted and points to "find my lost work"; exits 0.

- Text: "No interrupted GiTrust pipeline found for this repo. If you're looking for lost commits, try `gitrust "find my lost work"`." It is plain and gives the right next step.
- Exit 0 even though nothing was done. This conflicts with the "did nothing never exits 0" convention (same as M-25). Probably fine for a status query, but make it a deliberate decision.
- No first line naming what was understood, which is fine for a flag.
