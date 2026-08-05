# M-15 · Undo gate: four options, names the commit

| | |
|---|---|
| **LLM** | no |
| **Flagship** | — |
| **Result** | ✅ PASS (corrected after M-16 evidence) |
| **Run date** | 2026-08-04 |

## What this proves

Four options, names short oid + subject.

## Procedure

**Setup:**
```bash
mk_sandbox m15
echo v2 >> app.txt && git commit -qam "feat: the mistake"
```

**Steps:**
```bash
$GITRUST "undo"        # choose KEEP STAGED
git status; git log --oneline
```

**Expect:** ChoiceGate with **exactly four options** (keep staged / keep in files / inverse commit / discard); question names the short oid + "feat: the mistake". After keep-staged: changes staged, commit gone.

## Result

**✅ PASS. (Corrected: an earlier PARTIAL verdict here was based on a misread of the terminal log — the four options WERE present. See correction note.)**

**✅ Names the commit (key discoverability assertion):** the prompt was *"Undo **b1f6c0d "feat: the mistake"** — what should happen to its changes?"* — short oid **and** subject. Clean. ✅

**✅ Four options present.** The undo gate is an `inquire::Select` list with **exactly four** options — confirmed by direct screenshot evidence captured during M-16 on the same gate:
1. *Keep them staged — (soft reset) — the commit is removed, files stay ready to re-commit.*
2. *Keep them in files — (mixed reset) — re-stage what you want before committing.*
3. *Make an inverse commit (revert) — history is preserved; safe even after pushing.*
4. *Discard completely — (hard reset) — the changes are gone (reflog holds them ~90 days). Requires typing to confirm.*

**Correction note:** the M-15 run's captured log showed only the *"Keep them staged"* line because `inquire::Select` **collapses the list to the chosen row after selection** — the other three options scrolled away once keep-staged was picked. The initial verdict wrongly read that collapsed view as "only one option offered." M-16's screenshot (arrowing through the full list to reach Discard) proves all four render. Verdict corrected PARTIAL → PASS.

**✅ Keep-staged outcome correct:** after undo, `git status` shows `app.txt` **staged** ("Changes to be committed"); `git log` shows the commit **gone** (HEAD back to `32fdfdc base`). Verified `git status --porcelain` → `M  app.txt` (staged), HEAD `32fdfdc base`. Nothing lost, commit removed. ✅

**Cosmetic note (minor, not a failure):** in the collapsed selected-row view the label reads *"Keep them staged — keep them staged (soft reset)"* — the short label and the start of its description overlap. Purely cosmetic.

**Repro:** deterministic.

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
