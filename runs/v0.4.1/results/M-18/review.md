Verdict: PASS-WITH-NOTES
Summary: Halts safely with guidance, but first line misstates the request as "last commit".

- Output: "✗  Multi-commit undo isn't supported yet. Did you mean: squash the last 3 into one (gitrust "squash last 3"), revert a specific commit, or undo just the most recent (gitrust "undo")?" Exit 1, HEAD unchanged.
- The first line "✦  Undo the last commit · 1.8s" says what GiTrust understood, but the user asked for 3 commits. This is misleading, even though the halt came straight after.
- The "Did you mean" is a text error, not a menu, so the user has to retype. Only the squash option gives an example command; revert gives none.
