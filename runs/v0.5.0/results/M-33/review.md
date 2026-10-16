Verdict: PASS
Summary: [s] drops the push step and redraws a 2-step plan; the commit stays local (↑1), exit 0.

- "⚡  Commit and push everything", then an empty "? Commit message:" prompt (nothing drafted). The legend offers "[s] don't push" only while the plan has a push.
- After s: "↳ Not pushing this time — the commit stays local. Push later with gitrust "push"." The plan is redrawn as "Plan  · 2 steps" and the legend becomes "[Enter] run · [e] edit message · [q] cancel".
- Result: "→ Committed: local only (39657ba→cd388cf)", "✓ Done · 1 commit on main, ↑1 ↓0", "Next: gitrust "push" · changed your mind? gitrust "undo"". This is GiTrust's own summary, not git's "[main …]" output.
- v0.4.1 notes: the positive notes all still hold. The old 3-step plan is still on screen above the new one (it is a terminal log, not an in-place redraw). It reads fine because the "↳ Not pushing this time…" line sits between the two plans, so it isn't a defect.
