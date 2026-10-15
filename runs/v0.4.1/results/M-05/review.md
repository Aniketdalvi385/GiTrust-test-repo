Verdict: FAIL
Summary: Branch created; dirty switch is safe but shows a raw libgit2 error chain.

- `create branch feature-x` → one-step plan, "Created branch feature-x", exit 0.
- `switch to other` with an uncommitted edit to app.txt that the switch would overwrite: the edit survives and the run exits non-zero — the behaviour is safe.
- But the message is libgit2's: "✗  Failed to checkout 'other'" / "caused by: 1 conflict prevents checkout; class=Checkout (20); code=Conflict (-13)", printed twice. No plain explanation and no next step (commit or `gitrust "stash"` first). Same class as F2 (raw error chains). Reviewed by hand (the automatic check caught it).
