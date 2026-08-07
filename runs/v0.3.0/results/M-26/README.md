# M-26 · Clean-up gate + trash backup, nested dirs

| | |
|---|---|
| **LLM** | no |
| **Ollama** | on |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-07 13:31 |

## Notes
Cleanup gate states tracked/untracked COUNTS (1 tracked, 1 untracked) and names the trash-net in each consequence. Chose delete-untracked → junk/ removed from tree; nested file present + byte-path-identical at ~/.gitrust/trash/20260807-132721/junk/inner/file.txt; tracked mod untouched. Trash-net (clean path) + nested-dir recursion correct.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
