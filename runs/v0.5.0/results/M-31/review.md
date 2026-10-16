Verdict: PASS-WITH-NOTES
Summary: Esc at the undo menu: one calm "↪ Canceled — nothing was done.", exit 1, HEAD untouched; the only note is two menu hints cut with "…".

- Numbered menu, each row saying what it does, no Cancel row, "[1–9 or ↑↓ + Enter to choose · Esc cancel]". After Esc: `? Undo 449e227 "feat: the mistake" — what should happen to its changes? <canceled>` then "↪  Canceled — nothing was done." — calm, no error styling; exit 1; HEAD untouched.
- Polish: two hints are cut at the 110-column terminal — "its changes stay in your files, unstag…" and "· you'll type to con…"; a narrower terminal cuts more.
- v0.4.1 notes: numbered 4-row menu without a Cancel row, Esc named — still. Calm cancel, exit 1, HEAD unchanged — still. Hints cut with "…" ("unstag…", "you'll type to con…") — still there.
