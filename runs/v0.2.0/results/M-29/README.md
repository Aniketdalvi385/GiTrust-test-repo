# M-29 · Ollama down: graceful degrade

| | |
|---|---|
| **LLM** | — |
| **Flagship** | — |
| **Result** | ✅ PASS (graceful degrade + manual fallback) |
| **Run date** | 2026-08-05 |

## What this proves

Friendly error, status still instant.

## Procedure

**Setup:** `mk_sandbox m29`; **stop Ollama**.

**Steps:**
```bash
$GITRUST "what changed in the auth files?"   # forces LLM path
$GITRUST "status"                             # still instant
```

**Expect:** first fails with a friendly error naming the fix (start Ollama / run setup) — no panic; second still works instantly (⚡). **Restart Ollama after.**

## Result

**✅ PASS — graceful degrade is exemplary: friendly error + manual-mode fallback, and the fast path stays instant.**

**Setup note:** Ollama on this machine runs as a **Homebrew service** (`homebrew.mxcl.ollama` via launchd) — `pkill` couldn't take it down (the launchd watchdog revived it instantly, which invalidated a first attempt where the LLM request accidentally ran against a live model). Correct method: `brew services stop ollama`. Confirmed **"STILL DOWN after 3s"** before the real run.

**LLM request (Ollama genuinely down) — friendly + degrades to usable:**
- Error was human-readable and named the fix (two of them): *"⚠ LLM classification failed: Failed to connect to Ollama at http://localhost:11434/api/generate. Run `gitrust setup` to install and configure Ollama, or start it manually with `ollama serve`."* **No Rust backtrace / no raw panic.** ✅
- **Beyond the assertion — it doesn't dead-end:** *"Falling back to manual mode… LLM unavailable. Entering manual mode."* → presents a **manual git-operation picker** (git init / status / diff / branch / …). Selected `git diff` → worked (`* (instant)`, "No changes vs HEAD"). So the tool stays fully usable with no model — graceful degrade in the fullest sense. ✅

**Fast-path status — unaffected:**
- `gitrust "status"` → `* (instant)`, full status render, while Ollama down. Re-confirms the M-01 fast-path-has-no-model-dependency guarantee under genuine model-down conditions. ✅

**No panic anywhere. Ollama restarted cleanly** (`brew services start ollama` → "OLLAMA BACK UP ✓").

**Minor — exit-code (6th instance, softened).** `EXIT1=0` after the LLM-connection failure. Softer than M-17/M-27 because the run **recovered into manual mode** and completed an action, so the terminal state was arguably a success — but the initial "classification failed" is a degraded state a strict script wouldn't catch. Noted as a minor instance, not a hard strike. (`EXIT2=0` for status is correct.)

**Repro:** deterministic once Ollama is stopped at the service level (`brew services stop ollama`), NOT via `pkill`.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
