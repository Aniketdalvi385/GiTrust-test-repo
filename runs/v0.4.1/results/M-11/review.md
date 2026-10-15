Verdict: PASS
Summary: Commit mid-rebase refused clearly, naming the rebase options, exit 1.

- Output: "✗  A rebase is in progress. Back out with `gitrust "abort rebase"`, or resolve the conflicts and `gitrust "continue rebase"`." The message is plain and specific, with no "checkout a branch" misroute.
- Exit 1, instant, nothing changed. The first line "⚡  Commit everything" is printed before the refusal, which is slightly odd but harmless.
