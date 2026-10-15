Verdict: PASS-WITH-NOTES
Summary: Hook failure blocks commit and shows output, but Cancel row and misleading cancel text.

- Plan warns "Hook(s) present (pre-commit) — GiTrust will run them via system git." The step reads "hooks detected — using system git so they run." Failure shows "the pre-commit hook refused the operation: LINT FAILED". Exit 1, no commit.
- A "Pick one: Show / Cancel" menu appears. This has a "Cancel" row, which breaks the no-Cancel-row convention (Esc already cancels). "Show" re-prints output that is already on screen.
- Esc prints "  Canceled — nothing was done." without the "↪" marker. It is also untrue: "Staged all changes" already ran and the files stay staged. The text should say so.
- Error is printed twice ("LINT FAILED" appears in the step and again after the cancel). The snapshot/--recover lines are noisy for a hook failure that changed nothing but the index. "fix `commit` and continue:" has no clear next action.
