# M-00 · Binary version and help

| | |
|---|---|
| **Part** | 0 · Setup |
| **Model** | no |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:16 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ --version exits 0
- ✅ screen shows 'gitrust 0.'
- ✅ help exits 0
- ✅ screen shows 'status'
- ✅ no panic / raw error chain

## What a human should judge

Version matches the run folder; `gitrust help` reads as a useful cheat-sheet.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: Version 0.4.1 and a clear, accurate help cheat-sheet.

- `gitrust 0.4.1` exits 0; help exits 0 instantly, grouped by Look/Save/Share/Branches/Undo/Mid-rebase/Setup.
- Help states the conventions: "Esc cancels any prompt (nothing is changed)" and that --yes "never picks an option for you".
- Minor inconsistency: "gitrust recover --list" in the footer versus "Run gitrust --recover" in other messages.
