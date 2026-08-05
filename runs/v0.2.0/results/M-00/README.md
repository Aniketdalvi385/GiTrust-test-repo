# M-00 · Build, version, setup

| | |
|---|---|
| **LLM** | yes |
| **Flagship** | — |
| **Result** | ✅ PASS |
| **Run date** | 2026-07-31 |

## What this proves

Build/version/setup gate.

## Procedure

**Setup:** none (build already produced the 0.2.0 binary).

**Steps:**
```bash
$GITRUST --version        # must read: gitrust 0.2.0
$GITRUST setup            # verifies Ollama + pulls model if missing
```

**Expect:** version reads **0.2.0** (if it says 0.1.0 the Cargo.toml bump was missed). Setup verifies Ollama and the model, friendly confirmation. Fill the environment table in the report.

## Result

**PASS.** `gitrust --version` → `gitrust 0.2.0` (bump landed in the binary). `gitrust setup` reported: Ollama installed, Ollama running, model `qwen2.5:3b` ready, smoke test passed — friendly "Setup complete" confirmation. Both exited 0.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
