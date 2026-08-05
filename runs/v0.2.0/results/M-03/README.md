# M-03 · Commit with editable message

| | |
|---|---|
| **LLM** | yes |
| **Flagship** | — |
| **Result** | ✅ PASS |
| **Run date** | 2026-07-31 |

## What this proves

Editable message gate.

## Procedure

**Setup:** `mk_sandbox m03`.

**Steps:**
```bash
echo change >> app.txt
$GITRUST "commit this"
# when the editable-message gate appears, ALTER the draft before accepting
git log -1 --format=%s
```

**Expect:** preview restates the plan; message gate is editable; **your edited text** (not the draft) is the commit subject; post-check confirms.

## Result

**PASS.** The editable message gate worked as designed:
- Model drafted a subject (`fix(app.txt): add missing change line`), then presented `Commit message (edit or accept):` — genuinely editable.
- The tester's edited text was accepted, and `git log -1 --format=%s` printed **exactly the edited subject** (`fix(app.txt): add missing change line was the default message provided by the modal.`) — not the original AI draft. The edit-wins assertion holds.
- Preview restated the 2-step plan (stage → commit) with a snapshot oid before executing; post-commit confirmation showed the oid transition (7e1af7f→8617739) and `↑1 ↓0`.

**Observation (experience nit, not a failure):** the tool warned the subject was **84 chars (>72 recommended)** and then committed it anyway at 84 chars — the length warning is advisory, not a re-prompt/block. Reasonable, but a known-long subject sails through. Worth considering whether the gate should re-offer an edit on a warned subject.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
