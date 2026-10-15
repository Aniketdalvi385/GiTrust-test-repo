Verdict: PASS-WITH-NOTES
Summary: Conflict pauses calmly with exit 1 and continue works; raw git noise and stale warning.

- The pause message is good: "✗  Paused on conflicts in 1 file(s) — nothing is lost. Resolve them, then `gitrust "continue rebase"`, or `gitrust "abort rebase"`…". Exit is 1. It does not name the file, though the README asks for that.
- Raw git output leaks, and is garbled: "Auto-merging app.txtorigin/mainRebasing (1/1)", "error: could not apply…" and the hint: lines. This breaks the plain-message convention.
- On "continue rebase", a misleading banner appears: "⚠  An interrupted pipeline was found… Run 'gitrust --recover' to restore the repository to its pre-pipeline state." This is a normal, deliberate pause, and following the advice would undo the user's resolution. Worth fixing.
- Continue itself works: "Rebase continued", on main ↑1 ↓0, exit 0. This matches the automatic verdict.
