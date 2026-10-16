Verdict: PASS
Summary: gitrust 0.5.0; help is a clear, accurate cheat-sheet (unchanged from v0.4.1).

- `--version` prints "gitrust 0.5.0" (matches the run folder), exit 0; `help` exits 0 instantly.
- The help groups the instant phrases ("Look:        status · log · diff · show · branches · remotes · config" … "Mid-rebase:  continue rebase · skip rebase · abort rebase · abort merge") and states the rules plainly: "Esc cancels any prompt (nothing is changed)", "--yes skips prompts, but never picks an option for you and never skips a type-to-confirm", learned picks are "never for operations that discard or rewrite work".
- The model is described honestly ("A small local model picks from a fixed list of Git operations — it never invents a command"); scores stay behind "GITRUST_DEBUG=1 shows the model's scores". No op ids.
- v0.4.1 notes: "'gitrust recover --list' in the footer versus 'Run gitrust --recover' in other messages" — the footer is unchanged ("More: gitrust setup · gitrust aliases · gitrust recover --list · gitrust --help"), but no screen in this run prints `--recover` advice, and both commands exist (`recover --list` lists snapshots), so nothing on screen is wrong; not counted.
