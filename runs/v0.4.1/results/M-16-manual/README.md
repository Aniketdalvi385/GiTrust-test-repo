# M-16-manual · Undo → throw away: type to confirm, trash backup

| | |
|---|---|
| **Part** | 4 · Undo |
| **Model** | no |
| **Flagship** | ★ yes |
| **Run** | manual · 2026-10-15 18:22 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ commit gone
- ✅ working tree clean
- ✅ trash backup written
- ✅ screen shows 'backup'
- ✅ no panic / raw error chain

## What a human should judge

A typed confirmation before anything happens; the success line names the backup.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: By hand: typed confirmation, discard, backup named; risk text overstates the loss.

- Run by the owner and recorded: [`evidence/M-16-V.0.4.1.mov`](../../evidence/M-16-V.0.4.1.mov).
- Explanation block → `Type 'edd9e74' to DISCARD commit …` → plan → "A backup of the discarded changes is in ~/.gitrust/trash/20261015-182216 for 7 days."
- Copy contradiction (new, add to F17): the Risks line says "Any uncommitted work — staged or unstaged — is gone" and Recovery mentions only `git reflog`, while the plan warning and the result say uncommitted changes are backed up to ~/.gitrust/trash. The risk text should mention the backup.
- Confirmed twice — typed confirmation, then the plan's Enter (F9).
