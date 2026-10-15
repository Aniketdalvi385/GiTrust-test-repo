# M-23-manual · Deleted branch → find my lost work

| | |
|---|---|
| **Part** | 6 · Forensics |
| **Model** | no |
| **Flagship** | ★ yes |
| **Run** | manual · 2026-10-15 18:17 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ a rescue branch exists
- ✅ rescue branch at the lost commit
- ✅ HEAD untouched
- ✅ no panic / raw error chain

## What a human should judge

Lists the lost commit in plain words; restores it to a rescue branch; your current branch and files untouched.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: By hand: lost commit listed in plain words, restored to a rescue branch.

- Run by the owner and recorded: [`evidence/M-23-V.0.4.1.mov`](../../evidence/M-23-V.0.4.1.mov).
- "Lost & recoverable commits (restoring creates a rescue branch — your current work is never touched)" → "[1] just now — 'the work I'll lose' — 1 file" → "Recovered fbec8cb onto new branch `rescue/20261015-fbec8cb`. Your current branch and files are unchanged."
- The origin-story flow works end to end, by hand, in three keypresses.
