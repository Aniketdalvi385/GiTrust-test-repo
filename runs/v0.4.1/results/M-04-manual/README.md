# M-04-manual · Scoped push: only the login files

| | |
|---|---|
| **Part** | 1 · Everyday |
| **Model** | yes |
| **Flagship** | ★ yes |
| **Run** | manual · 2026-10-15 18:19 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ exits 0
- ✅ login.txt pushed
- ✅ readme.txt NOT pushed
- ✅ readme.txt still uncommitted
- ✅ no panic / raw error chain

## What a human should judge

Picker pre-selects the login files, shows +N −M and a reason per file; readme.txt not pre-selected; only login files reach the remote.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS
Summary: By hand: picker chose the login files; committed with own message and pushed.

- Run by the owner and recorded: [`evidence/M-04-V.0.4.1.mov`](../../evidence/M-04-V.0.4.1.mov).
- Plan: stage `auth_login.txt, login.txt` → commit "Login added to the application." → push; the legend offered `[e] edit message · [s] don't push` because the plan commits and pushes.
- "✓ Done · 1 commit on main, ↑0 ↓0" and the footer "changed your mind? gitrust "undo" (reverts it — it's pushed)" — the right undo for a pushed commit.
- Same as the automatic run; readme.txt stayed uncommitted.
