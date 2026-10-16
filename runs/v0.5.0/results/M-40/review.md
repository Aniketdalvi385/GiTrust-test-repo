Verdict: PASS
Summary: The clean tree is caught before any message prompt with a plain "Nothing to commit", exit 1.

- "✗  Nothing to commit — the working tree is clean." There was no message prompt. Exit 1 is correct: the operation didn't happen (convention 7).
- v0.4.1 notes: the core behaviour is unchanged and right. The "*  Commit everything" marker is still there. It is the deliberate ASCII marker for non-terminal output (* for ⚡), so it isn't a defect.
