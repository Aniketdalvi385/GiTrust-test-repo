# M-20 · Amend-on-pushed: escalation + lease (flagship)

| | |
|---|---|
| **LLM** | yes |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-07 13:31 |

## Notes
FLAGSHIP now works end-to-end: 'fix the last commit message to \'typo message fixed\'' fast-path (*) → amend recognized → detected published commit → force-push escalation with the ⛔ irreversible block → TypeToConfirm on branch name 'main' → amend + `--force-with-lease` (log shows 'forced update', NO bare --force). Remote subject is now 'typo message fixed'. The whole flow that was unreachable in v0.2 is live. P2 amend fix confirmed.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
