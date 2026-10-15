Verdict: PASS
Summary: --yes refuses to pick an undo mode, lists choices, exits 1.

- Message: "✗  --yes won't choose for you — Undo f143c04 "feat: the mistake" — what should happen to its changes?" then lists all four choices and "Run it interactively (without --yes) to pick one, or say more precisely what you want." Plain and actionable.
- Exit 1, HEAD untouched. No panic or raw chain.
- Minor: first line uses "*" instead of ⚡/✦/◇ (probably a no-tty variant of the marker). The choice list also carries the "⚠⚠" glyph inline.
