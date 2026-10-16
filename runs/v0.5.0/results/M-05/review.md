Verdict: PASS
Summary: Branch created; the dirty switch is refused before any plan in one plain sentence naming app.txt; "Already on main." exits 0.

- "create branch feature-x": plan "●  branch    feature-x", Enter, "→ Created branch feature-x", "✓ Done · on main, ↑0 ↓0" (honest that it didn't switch); exit 0.
- "switch to other" with an edit to app.txt: refused before any plan, once, with the way out — "✗  Switching to other would overwrite your uncommitted changes to app.txt. Commit them (gitrust "commit everything") or stash them (gitrust "stash") first." Exit 1; the edit survives. (The "everyt/hing" break is the 110-column screen wrapping.)
- "switch to main" while on main: "Already on main.", exit 0 (D4).
- v0.4.1 notes: the FAIL is fixed — the "Failed to checkout 'other'" / "caused by: 1 conflict prevents checkout; class=Checkout (20); code=Conflict (-13)" chain, printed twice, is replaced by the single sentence above naming the file and the next step. Branch creation unchanged and fine.
