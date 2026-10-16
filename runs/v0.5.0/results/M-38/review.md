Verdict: PASS
Summary: One plain line, exit 1, and the advice now says --yes won't choose instead of suggesting it.

- "✗  This needs a choice, and there's no terminal to ask in (input or output is redirected). Run it in a terminal to choose — --yes won't choose for you." One line, no "caused by", exit 1 (0.1s).
- v0.4.1 notes: the misleading "…and add --yes" advice is fixed. It now reads "Run it in a terminal to choose — --yes won't choose for you." The "*  Undo the last commit" marker is still there. It is deliberate: piped output uses ASCII markers (* for ⚡, + for ✦, > for ◇). It is a little inconsistent that the "✗" on the next line isn't converted the same way, but that isn't a defect.
