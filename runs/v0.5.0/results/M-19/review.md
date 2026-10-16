Verdict: PASS
Summary: Squash asks for the message on an empty prompt with the three subjects listed above it; one Enter at a one-line plan; tree identical, exit 0.

- D3 as planned: "The 3 commits being combined, newest first:" · commit 3 · commit 2 · commit 1, then an empty "? Squashed commit message (3 commits):" with "[Enter to continue · Esc to cancel]". The commit's message is exactly "three in one".
- The plan is one line, `●  squash    last 3 → "three in one"  ⚠`, confirmed once with "[Enter] run · [q] cancel". Result `✓  squash    last 3 → "three in one"` / "→ Squashed the last 3 commits into one" / "✓ Done · on main, ↑1 ↓0" — right (three unpushed commits became one). No git output on the step. "⚡  Squash the last 3 commits" names what was understood.
- v0.4.1 notes: pre-filled joined subjects — fixed (empty prompt, subjects listed above it). Typed text glued onto the pre-fill and a multi-line plan — fixed (`last 3 → "three in one"`). Stray `○  squash    last 3 → "commit 3 / commit 2` — fixed (the legend is followed directly by the ✓ line). Behaviour — still right: 2 fewer commits, tree identical, exit 0.
