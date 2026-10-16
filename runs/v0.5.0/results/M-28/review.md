Verdict: PASS-WITH-NOTES
Summary: Nothing interrupted, points to "find my lost work", now exits 1 (D4); "pipeline" is an internal word.

- "No interrupted GiTrust pipeline found for this repo. If you're looking for lost commits, try `gitrust "find my lost work"`." — one plain line with the right next step; exit 1, an operation (a restore) that didn't happen, per D4.
- Copy: "GiTrust pipeline" is the internal name; users see plans and operations (e.g. "Nothing to recover — no GiTrust operation was interrupted in this repo.").
- v0.4.1 notes: plain text with the right next step — still. Exit 0 — fixed (exit 1, the D4 rule). No first line naming what was understood — unchanged, still fine for a flag.
