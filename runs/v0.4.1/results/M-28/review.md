Verdict: PASS-WITH-NOTES
Summary: Says nothing interrupted and points to "find my lost work"; exits 0.

- Text: "No interrupted GiTrust pipeline found for this repo. If you're looking for lost commits, try `gitrust "find my lost work"`." It is plain and gives the right next step.
- Exit 0 even though nothing was done. This conflicts with the "did nothing never exits 0" convention (same as M-25). Probably fine for a status query, but make it a deliberate decision.
- No first line naming what was understood, which is fine for a flag.
