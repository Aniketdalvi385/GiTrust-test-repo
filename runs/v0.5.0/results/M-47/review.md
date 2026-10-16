Verdict: PASS
Summary: F4 is fixed: "stash pop" with no stash is blocked before any plan with "There are no stashed changes to bring back.", exit 1, and the edit is untouched.

- "⚡  Restore stashed changes" then "✗  There are no stashed changes to bring back." One plain line: no plan, no libgit2 "refs/stash" error chain, exit 1 in 0.5s. The uncommitted edit is untouched ("M app.txt" before and after).
- The optional "v0.4 flow: a plan for a pop that can't work" step only re-captured the same final screen; no plan ever appeared.
