# M-29 · Ollama down: graceful degrade

| | |
|---|---|
| **LLM** | dash |
| **Ollama** | off |
| **Result** | ✅ PASS |
| **Run** | v0.3.0 · 2026-08-07 15:11 (Ollama stopped — degrade path now exercised) |

## What to look for
Ollama must be STOPPED. First command should fail friendly (name the fix, no panic); a follow-up status must still work instantly.

## Command
```bash
$GITRUST "what changed in the auth files?"
```

## Notes
PASS — with Ollama actually stopped this time, the graceful-degrade path is genuinely exercised (the earlier SKIP was because Ollama was still up). Live: 'LLM classification failed: Failed to connect to Ollama at http://localhost:11434 … Run `gitrust setup` … or `ollama serve`. Falling back to manual mode.' — friendly, names the fix, no panic. Then the manual-mode operation picker appeared and 'git status' ran ⚡ (instant), fast-path, no LLM dependency. Degrade is clean and recovery is immediate.

## Evidence
- [`commands.sh`](commands.sh) — setup + command
- [`output.log`](output.log) — live session transcript + post-facts
