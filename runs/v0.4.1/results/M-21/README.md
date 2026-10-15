# M-21 · A failing pre-commit hook blocks the commit

| | |
|---|---|
| **Part** | 5 · Hooks |
| **Model** | yes |
| **Flagship** | no |
| **Run** | auto · 2026-10-15 17:53 |
| **Automatic checks** | ✅ all passed |

## Checks

- ✅ non-zero exit
- ✅ screen shows 'LINT FAILED'
- ✅ no new commit
- ✅ no panic / raw error chain

## What a human should judge

Says hooks were detected; the hook's output is shown; nothing committed; exit ≠ 0. Note: after the failure a 'Pick one: Show / Cancel' menu appears.

## Evidence

- [`screens.txt`](screens.txt) — every screen, run by run
- [`result.json`](result.json) — checks, exit codes, timings

## Review

Verdict: PASS-WITH-NOTES
Summary: Hook failure blocks commit and shows output, but Cancel row and misleading cancel text.

- Plan warns "Hook(s) present (pre-commit) — GiTrust will run them via system git." The step reads "hooks detected — using system git so they run." Failure shows "the pre-commit hook refused the operation: LINT FAILED". Exit 1, no commit.
- A "Pick one: Show / Cancel" menu appears. This has a "Cancel" row, which breaks the no-Cancel-row convention (Esc already cancels). "Show" re-prints output that is already on screen.
- Esc prints "  Canceled — nothing was done." without the "↪" marker. It is also untrue: "Staged all changes" already ran and the files stay staged. The text should say so.
- Error is printed twice ("LINT FAILED" appears in the step and again after the cancel). The snapshot/--recover lines are noisy for a hook failure that changed nothing but the index. "fix `commit` and continue:" has no clear next action.
