Verdict: PASS
Summary: Esc at the undo menu cancels calmly, exit 1, HEAD untouched.

- Numbered 4-option menu ("[1–9 or ↑↓ + Enter to choose · Esc cancel]") with no Cancel row; help line mentions Esc.
- After Esc: "? Undo f4f7e88 ... <canceled>" then "↪  Canceled — nothing was done." Exit 1, HEAD unchanged.
- Some row descriptions are truncated with "…" (e.g. "unstag…", "you'll type to con…") at the test terminal width; cosmetic only.
