Verdict: PASS
Summary: Revert succeeds past the pre-commit hook, as git does; one Enter at a plan that names the commit's subject; clean step output, exit 0.

- "⚡  Revert the last commit", then a plan naming the commit by subject — `●  revert    c2d58f9 "to be reverted"  ⚠` — and only "[Enter] run · [q] cancel"; no (Y/n) anywhere.
- Result `✓  revert    c2d58f9 "to be reverted"` / `→ Reverted c2d58f9 "to be reverted" (inverse commit added)` / "✓ Done · on main, ↑2 ↓0" — right (the commit and its revert are both unpushed). No "[main …] Revert" or "delete mode" lines. One new commit, other.txt gone, exit 0.
- v0.4.1 notes: "? Revert a7ec361 with a new inverse commit? (Y/n)" before the plan — fixed (the plan is the only question). Git output on the step line — fixed. Behaviour — still right. Prompt named only the SHA — fixed (`c2d58f9 "to be reverted"` in the plan and the result).
