Verdict: PASS-WITH-NOTES
Summary: --yes refuses to choose an undo mode, lists the four choices, exit 1, HEAD untouched; the piped first line still uses "*" for ⚡.

- Right: `✗  --yes won't choose for you — Undo e4bfef2 "feat: the mistake" — what should happen to its changes?`, then "Choices: Undo, keep the changes staged · Undo, keep the changes in my files · Undo with a revert commit · Undo and throw the changes away  ⚠⚠" and "Run it interactively (without --yes) to pick one, or say more precisely what you want." One message, no error chain; exit 1; HEAD untouched.
- Polish: the first line is "*  Undo the last commit". With output piped, GiTrust swaps the engine glyph for ASCII (no colour → "*"), yet the next line prints "✗" and "⚠⚠" in Unicode anyway — the fallback only loses what ⚡ means. An uncoloured ⚡ would do.
- Copy nit: the menu question is pasted into the refusal — `— Undo e4bfef2 "feat: the mistake" — what should happen to its changes?` (two dashes, a question inside a refusal). F15 gave the model-down refusal its own sentence; this one could have one too, e.g. `--yes won't choose how to undo e4bfef2 "feat: the mistake".`
- v0.4.1 notes: plain refusal, choices listed, exit 1 — still right. "*" instead of ⚡/✦/◇ — still there ("*  Undo the last commit"). "⚠⚠" inline in the choice list — still there; harmless, it marks the destructive choice as the menu does.
