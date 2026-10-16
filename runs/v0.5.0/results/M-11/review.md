Verdict: PASS
Summary: Commit request mid-rebase refused in one plain line naming continue/abort; exit 1, instant.

- "commit my changes" → "⚡  Commit everything" then "✗  A rebase is in progress. Back out with `gitrust "abort rebase"`, or resolve the conflicts and `gitrust "continue rebase"`." — about the rebase, never "checkout a branch"; exit 1 in 0.0s; nothing changed; no error chain.
- v0.4.1 notes: refusal unchanged and right. The "⚡  Commit everything" line before the refusal (called "slightly odd") is the convention — the first line names what was understood — so not counted.
