Verdict: PASS
Summary: A polite refusal in 1.6s pointing at examples and `gitrust help`, exit 1.

- "✗  That doesn't look like a Git request. Try e.g. "show status" or "push my commits" — or `gitrust help` for phrases that always work." One plain line, no error chain, exit 1. There is no "understood" first line, which is right because nothing was understood.
- v0.4.1 notes: the 14.3s delay is fixed. This run took 1.6s ("exit=1  1.6s"), and the v0.4.1 report traced the delay to shards sharing the model. The mid-word break "for p / hrases" is still there, but it is the 110-column terminal soft-wrapping one long line (no text is lost), not GiTrust output, so it isn't a defect.
