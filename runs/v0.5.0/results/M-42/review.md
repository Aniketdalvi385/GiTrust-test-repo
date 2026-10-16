Verdict: PASS
Summary: Every phrase in help's Look section works instantly with the model down; the help text matches the v0.5.0 conventions.

- Help lists "Look:        status · log · diff · show · branches · remotes · config". With the model down, log, branches, current branch, remotes, config and diff each ran in 0.0s with exit 0 ("*  Show history", "*  List branches", "*  List remotes", "*  Show Git settings", "*  Show changes").
- The help copy fits v0.5.0: "Esc cancels any prompt (nothing is changed)", "--yes … never picks an option for you and never skips a type-to-confirm", and "GITRUST_DEBUG=1 shows the model's scores".
- v0.4.1 notes: the piped "*" marker is still there, and deliberate (ASCII marker for non-terminal output). "current branch" still shows "*  List branches" (the full list with "* main" marked). That is acceptable because the echo honestly says what ran.
