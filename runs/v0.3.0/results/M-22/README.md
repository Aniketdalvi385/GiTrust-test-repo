# M-22 · Revert parity: succeeds despite the same hook

| | |
|---|---|
| **LLM** | no |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-07 13:31 |

## Notes
Revert SUCCEEDED despite the identical failing pre-commit hook (inverse commit '317f629 Revert "to revert"' exists) — matches real git, where revert doesn't run pre-commit. Parity with M-21 proven: commit blocked, revert allowed.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
