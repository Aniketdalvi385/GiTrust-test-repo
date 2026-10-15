Verdict: PASS-WITH-NOTES
Summary: One plain line, exit 1; piped first line shows "*" not ⚡.

- "✗  This needs an answer, and there's no terminal to ask in (input or output is redirected). Run it in a terminal — or, in a script, say it precisely enough to need no choice and add --yes." One readable line, no "caused by", exit 1.
- Minor: the advice "add --yes" is misleading for undo, since --yes never picks an option (M-29 says so). Also the "*  Undo the last commit" marker is ASCII in pipe mode instead of ⚡.
