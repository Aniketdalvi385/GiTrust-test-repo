Verdict: PASS-WITH-NOTES
Summary: Friendly not-a-repo message with exit 1; piped first line uses "*" marker.

- "✗  Not inside a git repository. Run 'gitrust "initialize a repository"' or 'git init' first." is plain, specific and exits 1.
- First line is "*  Show status" rather than "⚡  Show status". Piped runs appear to use an ASCII "*" in place of the ⚡/✦ markers; harmless, but a small deviation from the stated convention (applies to all pipe runs).
