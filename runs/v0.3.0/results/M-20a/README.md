# M-20a · Amend-on-pushed — "fix the last commit message to …"

| | |
|---|---|
| **LLM** | yes |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-10 12:13 |

## Notes
Fast-path (⚡) → published-detection → TypeToConfirm(branch) → --force-with-lease (log: "forced update", no bare --force). Remote subject = "typo message fixed". Flagship works.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
