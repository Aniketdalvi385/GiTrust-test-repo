# GiTrust v0.3.0 — Fix Plan

**Source of failures:** the v0.2.0 manual acceptance run ([`../v0.2.0/REPORT.md`](../v0.2.0/REPORT.md)) — 19 PASS / 4 PASS-with-defects / 8 FAIL.
**Goal:** close every defect the run surfaced, rebuild the binary, and re-run the full M-00…M-30 suite into `runs/v0.3.0/` before the tool goes public.

> **Read this first — a ground-truth caveat.** The v0.2.0 binary that was tested is **behind the current `gitrust/src/` working tree**. Before planning, I re-read the source. Some failures are **already fixed in code but not yet in a rebuilt binary**; others are **still present**. Each item below is tagged accordingly. **No fix is claimed done until a rebuilt binary re-passes its test.**

---

## Priority order (plan-review lens: data-loss & exit-honesty first)

| # | Cluster | Tests | Severity | Source state |
|---|---|---|---|---|
| **P0** | Reset phantom-op (destructive op that lies) | M-16, M-19 | 🔴 Critical | **Still broken** |
| **P1** | Systemic exit-0 on every failure | M-08, M-17, M-21, M-22, M-27, M-29, M-30 | 🔴 Critical | **Likely already fixed — must verify** |
| **P2** | Argument / target extraction from phrase | M-04, M-05, M-10, M-19, M-20 | 🟠 High | Still present |
| **P3** | Snapshot lifecycle nag after pause/continue/abort | M-08, M-09, M-19, M-21 | 🟡 Medium | Needs check |
| **P4** | Redirect drops the original intent | M-13 | 🟡 Medium | Still present |
| **P5** | Copy / cosmetic defects | M-02, M-03, M-06, M-07, M-08, M-12, M-16, M-17 | 🟢 Low | Mixed |

---

## P0 — Reset execution is a phantom no-op 🔴

**Symptom (M-16, M-19):** `reset --hard` (undo→discard) and `reset --soft` (squash) both print `→ reset (…)` / `✓ Done`, but **HEAD never moves**. M-16 additionally claimed a trash backup that was never written.

**Root cause — located in source.** `Git2Operations::reset` at [`git_ops.rs:722-744`](../../../Glit/gitrust/src/git_ops.rs) peels the current HEAD to a commit and then resets **to that same commit**:

```rust
let head = repo.head()?;
let commit = head.peel_to_commit()?;          // <- current HEAD
repo.reset(commit.as_object(), reset_type, None)?;   // <- reset HEAD to HEAD = no-op
```

The `Reset { mode }` PipelineStep ([`commands.rs:119`, `:302`](../../../Glit/gitrust/src/commands.rs)) carries **only `mode`, no target oid**. So a `reset --hard`/`--soft` genuinely runs — successfully — but to the place HEAD already is. The preview ([`agent.rs:3313`](../../../Glit/gitrust/src/agent.rs)) even prints *"Will move HEAD back from X"*, which the executor never honors.

**The trash "false backup" (M-16) is a smaller, separate bug.** `backup_before_destroy` ([`git_ops.rs:279`](../../../Glit/gitrust/src/git_ops.rs)) correctly returns `Ok(None)` when the destroy-set is empty (clean tracked tree → nothing to back up → no dir, which is *correct*). The defect is only that the **success copy prints the backup line unconditionally** instead of from the returned `Option<PathBuf>`.

**Fix:**
1. **Give `Reset` a target.** Add `to_oid: String` to `PipelineStep::Reset` (both enum copies at `commands.rs:119` and `:302`). Undo→discard sets it to `HEAD~1`; squash sets it to `HEAD~N`. Reset **to that oid**, not to `head.peel_to_commit()`.
   - *Better:* route the destructive undo-discard through the existing, already-correct `Undo { to_oid, … }` primitive ([`commands.rs:322`](../../../Glit/gitrust/src/commands.rs)) family rather than the target-less `Reset`, and reserve `Reset { mode, to_oid }` for cleanup/squash. The `Undo` step already does target-based reset correctly — the discard path simply doesn't use it.
2. **Squash must actually squash (M-19).** Confirm "squash the last N" routes to the existing `SquashLastN` step ([`commands.rs:195/367`](../../../Glit/gitrust/src/commands.rs)) — the step is correct ("soft reset to HEAD~N + one commit"); the classifier just isn't reaching it (see P2). A bare `Reset` can never squash (no re-commit).
3. **Report outcomes from real results.** Emit the `reset (…)` / trash-backup success lines from the operation's actual `Result`/returned `Option<PathBuf>`, not from step metadata. If the backup was `None`, don't claim one.

**Verify (test-first):** red tests before the fix —
- undo→discard on `HEAD` with one commit ahead ⇒ after: `git rev-list --count HEAD` dropped by 1, commit gone, exit 0 only on real success.
- squash last 3 (three commits, different files) ⇒ count −2, `HEAD^{tree}` unchanged, **one** new commit exists.
- hard-reset with real tracked modifications ⇒ trash dir **exists** and is byte-identical; success line names it. Clean tree ⇒ **no** backup line printed.

---

## P1 — Systemic exit-0 on every non-success path 🔴 (verify-first)

**Symptom:** confirmed **7×** (M-08 paused rebase, M-17 refused undo, M-21 hook-blocked commit, M-22 failed revert, M-27 fail-closed refusal, M-29 LLM-connection failure, M-30 not-a-repo) — the `✗` glyph prints but the process exits **0**, so `gitrust … && next` proceeds after a failure.

**Ground truth — largely already fixed in current source.** `main()` ([`main.rs:88-98`](../../../Glit/gitrust/src/main.rs)) already does `eprintln!("✗ …")` + `std::process::exit(1)` on `Err`. The two paths I checked already return `Err`:
- not-a-repo → [`agent.rs:89-92`](../../../Glit/gitrust/src/agent.rs) `return Err(...)` (covers **M-30**).
- situation-gate Block → [`agent.rs:153-158`](../../../Glit/gitrust/src/agent.rs) `return Err(...)`, with the comment *"Returning Ok exited 0 and let scripts read a refused, never-executed op as success."*

So the top-level seam is right; the remaining question is whether **every** refusal/abort/block path now bubbles `Err`. **Do not assume — verify each of the 7 by rebuilding and re-testing.**

**Fix (only where a gap survives the rebuild):** ensure each of these returns `Err` (nonzero), not `Ok(())`:
- `--yes` refusals in [`confirm.rs`](../../../Glit/gitrust/src/confirm.rs) `AutoConfirmGate` (M-17).
- pre-check `Block` in `run_pre_checks` / hook-blocked commit (M-21).
- revert on dirty tree / git status 128 (M-22).
- fail-closed trash refusal (M-27) — already `Err` from `backup_before_destroy?`, confirm it isn't swallowed upstream.
- LLM-connection failure (M-29) — confirm the classifier error propagates rather than degrading to `Ok`.
- paused rebase (M-08) — a conflict pause is *not success*; return `Err` (and suppress the raw `git rebase --continue/--skip/--abort` hint dump above the calm message).

**Verify:** `gitrust <case>; echo $?` ⇒ nonzero for all 7. Add a `#[test]` per path asserting the function returns `Err`.

---

## P2 — Argument / target extraction from the phrase 🟠

**Symptom:** requests carrying a target/scope/count/message get the argument dropped or the whole intent misrouted.

| Test | Phrase | What happened | Should |
|---|---|---|---|
| M-04 | "push the login changes" | routed as bare `push`; committed **all** files incl. `readme.txt` | scope → login files only via the file-relatedness resolver + multi-select |
| M-05a | "create branch feature-x" | branch **listing** + "Nothing to do" | create `feature-x` |
| M-05b | "checkout main" | "✗ No target branch specified" (name was in the phrase) | checkout `main` (fast-path) |
| M-10 | "sync with main" | classified as read-only **status** | rebase onto `origin/HEAD` |
| M-19 | "squash the last 3 commits" | single-commit soft reset (count dropped) | route to `SquashLastN { n: 3 }` |
| M-20 | "fix the last commit message to '…'" | flaky: new-commit vs amend; quoted message dropped; clarify-loop stalls | amend, use the quoted message |

**Root causes — located:**
- **Fast-path gaps.** `try_canonical("create branch foo")` deliberately returns `None` (test at [`intent.rs:1197`](../../../Glit/gitrust/src/intent.rs)) → falls to the LLM, which drops the trailing name. Same for `checkout <name>` with an argument. These arg-carrying forms need a **deterministic parse** (prefix-match + capture the trailing token) so they never round-trip the model and never lose the arg. A plain `checkout <branch>` should be `⚡` fast-path, not `◉`.
- **Classifier extraction gaps** ([`prompts.rs`](../../../Glit/gitrust/src/prompts.rs)). The LLM prompt must be told to extract, into structured fields: scope pattern (M-04 → `FileSelection::Pattern`), sync target (M-10), squash count (M-19 → `SquashLastN.n`), and the quoted new message (M-20 → `Amend.message`). Confirm each `IntentType` variant actually carries the field (`SquashLastN` and `Amend` already do; verify `Push`/scoped-commit carries an optional scope).
- **Clarification loop never converges (M-20).** Once amend intent is recognized, the loop re-asks "provide more context?" instead of presenting the amend plan. Fix `clarification_loop` to **offer the resolved plan directly** once a confident intent + argument are in hand, rather than re-looping.

**Fix order:** (a) add deterministic fast-path arg-capture for `create branch <name>` / `checkout <name>` / `switch to <name>` — cheapest, kills M-05 and the latency miss; (b) prompt-engineer the four extraction slots and add few-shot examples for the small qwen2.5:3b model; (c) fix the clarify-loop convergence for M-20.

**Verify:** M-04 pushes only login files; M-05 creates the branch and checks out by name on fast-path; M-10 rebases; M-19 collapses 3→1; M-20 amends with the quoted message and reaches the force-push escalation. (LLM-path tests: assert the parsed `IntentType`, which is deterministic given a fixed model response — mock the classifier in unit tests.)

---

## P3 — Snapshot lifecycle nag 🟡

**Symptom (M-08, M-09, M-19, M-21):** pause/continue/abort/blocked-commit leave a `~/.gitrust/snapshots/*.json` behind → every later command (even read-only `status`) nags *"interrupted pipeline — run --recover"*, pointing at `--recover` which could undo completed work.

**Fix:** on a **completed** continue/abort (and on a blocked commit that never mutated), delete the snapshot. The snapshot must represent *genuinely* interrupted state only. Check `check_for_interrupted` / the recovery lifecycle in [`recovery.rs`](../../../Glit/gitrust/src/recovery.rs) + the rebase-continue/abort handlers in [`agent.rs`](../../../Glit/gitrust/src/agent.rs).

**Verify:** after a full rebase-continue, `ls ~/.gitrust/snapshots/` is empty and the next `status` shows no nag.

---

## P4 — Redirect drops the original intent 🟡

**Symptom (M-13):** `commit this` in detached HEAD → branch-here rescue creates the branch **but never commits**; the user is left believing they committed. Same family as M-08/M-09 "intent not resumed after redirect."

**Fix:** after the detached-HEAD rescue (`handle_detached_head_rescue`, [`agent.rs`](../../../Glit/gitrust/src/agent.rs)) creates/switches to the branch, **resume the original intent** (the commit) rather than returning. Thread the original `IntentType` into the rescue and re-dispatch on success.

**Verify:** M-13 ends on `rescue-work` **with the commit made** (`git log -1` = the new commit, tree clean).

---

## P5 — Copy & cosmetic 🟢

Batch these; each is a one-line string or small logic tweak in [`copy.rs`](../../../Glit/gitrust/src/copy.rs) / `agent.rs`:

- **M-08/M-09** conflict count says "0 file(s)" and names none → report the real count and name the conflicted file(s).
- **M-16** TypeToConfirm says "type the **branch name**" but asks for the **commit oid** → fix the string.
- **M-17** undo refusal recites "rebase vs merge **strategy**" (wrong op) → give undo its own refusal copy.
- **M-12** commit keeps `# Conflicts:` comment lines in the merge message → strip them.
- **M-02** marker glyph: binary prints `@` for the LLM path; suite text expected `◉` → align (fix whichever is canonical; the binary uses `⚡`/`◉` per `copy.rs` — confirm and update the suite text if the glyph is intended).
- **M-06/M-07** "consider pulling first" shown *inside* a plan that already rebases/merges → suppress the redundant nudge.
- **M-03** 84-char commit subject warned but committed anyway → re-prompt (or hard-wrap) instead of pass-through.

---

## Execution sequence

1. **P0 reset** — write the three red tests, fix the target-oid, watch green. (Highest user-harm: a destructive op that lies.)
2. **P1 exit codes** — rebuild, re-run the 7 cases; fix only surviving gaps; add per-path `Err` tests.
3. **P2 arguments** — fast-path arg-capture → prompt extraction → clarify-loop convergence.
4. **P3/P4/P5** — snapshot lifecycle, redirect-resume, then the copy batch.
5. **Gate:** `cargo test` (all, incl. new red-turned-green), `cargo clippy` clean, `cargo fmt --check`.
6. **Rebuild `--release`**, confirm `gitrust --version` = `0.3.0`, then **re-run M-00…M-30** into `runs/v0.3.0/results/` and write `runs/v0.3.0/REPORT.md`. Public-release gate: **0 FAIL, 0 critical defects.**

---

## Progress log

### ✅ P0 — Reset phantom-op — **FIXED** (2026-08-05)

Root cause was exactly as diagnosed: `Git2Operations::reset` peeled the current HEAD and reset **to that same commit** because `PipelineStep::Reset` carried no target. A commit-drop is a reset to the *parent*, so every undo→discard / undo→keep-in-files silently no-op'd.

**Changes (all in `gitrust/src/`):**
- `commands.rs` — `PipelineStep::Reset` gained `to_oid: Option<String>` (parent oid to drop a commit; `None` = reset to HEAD, i.e. discard a dirty working tree while keeping the commit).
- `git_ops.rs` — `reset` / `reset_with_trash_root` take `to_oid` and resolve the real target; return `Option<PathBuf>` (the actual backup dir, or `None` when the destroy-set was empty).
- `agent.rs` — undo→Discard and undo→KeepInFiles now pass the **parent** oid; cleanup→Tracked and plain "reset" pass `None` (keeps the M-26 behavior). The trash-backup success note now prints **only when a backup was actually written** (diffing the trash dir before/after), naming the real subdir — fixing M-16's false-backup claim.

**New regression tests (red→green):**
- `reset_hard_to_parent_drops_the_commit` — HEAD actually moves to the parent (M-16).
- `reset_mixed_to_parent_uncommits_but_keeps_files` — keep-in-files works.
- `reset_hard_to_head_still_discards_dirty_tree` — M-26 not regressed.
- Strengthened `undo_gate_offers_four_options…` to assert the discard step targets the parent oid, and the keep-in-files case targets `Some(_)`.

**Verification:** `cargo test` → **195 passed / 0 failed**; `cargo fmt --check` clean; no new clippy lints from the change (the two `RecoveryAction` "never read" warnings pre-date this work). **Note:** the fix is in source; the released binary must be rebuilt (`cargo build --release`) before M-16/M-19 are re-tested in the v0.3.0 suite. M-19 also needs P2 (classifier must route "squash the last 3" to `SquashLastN`, which is itself correct) to fully pass.

### ✅ P1 — Exit codes — **VERIFIED CORRECT** + one real copy bug fixed (2026-08-05)

**The headline exit-0 finding was a measurement artifact, not a tool bug.** Re-tested the release binary capturing gitrust's *own* exit code (not a piped `head`/`tee`'s):

| Case | gitrust exit |
|---|---|
| M-30 not-a-repo | **1** ✅ |
| M-17 `--yes` undo refusal | **1** ✅ |
| M-22 revert (dirty/non-TTY) | **1** ✅ |

Source confirms every refusal/block/error path returns `Err`, and `main()` maps `Err → std::process::exit(1)`: not-a-repo (`agent.rs:89`), situation-gate block (`agent.rs:158`), pre-check block (`agent.rs:1937` `return Err("Pre-checks blocked execution.")`), all `AutoConfirmGate` refusals (`confirm.rs:356/372/380`, each `Err`), revert failure (`git_ops.rs:1494`, propagates), LLM-connection failure (`intent.rs:846-867`, `Err("Failed to connect to Ollama…")`). **The original "exit 0" readings came from `echo $?` after a pipe** (`gitrust … | head` / the `run()` tee), where `$?` reflects the last pipe stage, not gitrust. Lesson for the v0.3.0 re-run: capture `${PIPESTATUS[0]}` or run gitrust unpiped.

**Real bug found and fixed (M-17 Defect 2):** the `--yes` ChoiceGate refusal hardcoded *"cannot choose a reconciliation strategy (rebase vs merge)"* for **every** gate, so `--yes undo` cited a rebase-vs-merge strategy for an op with neither. Fixed `confirm.rs` to **echo the actual gate question**, so it reads correctly for undo / cleanup / reconcile alike. Now: `--yes undo` → *"cannot answer this choice for you: 'Undo ba7d2f0 "to undo" — what should happen to its changes?'"*. Updated the two tests that asserted the stale wording. `cargo test` 195/0, fmt clean.

> Still to re-test with Ollama up in the v0.3.0 suite: M-08 (paused rebase should exit nonzero + suppress the raw git hint dump) and M-29 (LLM-down). Source shows both return `Err`; empirical confirmation deferred to the full re-run.

### 🔨 P2 — Argument extraction — **fast-path wins landed** (2026-08-05)

Per the "fast-path first" decision, the deterministic (offline-testable) captures are done; the LLM-prompt slots (M-04/10, amend clarify-loop M-20) remain.

**Done — `intent.rs` `try_canonical_parameterized`:** a new deterministic prefix/pattern capture layer, tried after the fixed-phrase whitelist and before any LLM round-trip.
- **M-05 create-branch / checkout — FIXED.** `create branch <name>` / `new branch <name>` / `checkout <name>` / `switch to <name>` now capture a single git-legal token → `Branch{name}` / `Checkout{target}`. Live-verified on the release binary: both run **fast-path `*` (instant)**, extract the name, and act (branch created; switched to main) — was: branch-listing + "No target branch specified", and an unnecessary LLM round-trip.
- **M-19 squash routing — FIXED (routing half).** `squash [the] last N [commits]` / `combine my last N commits` capture N deterministically → `SquashLastN{n}`, off the flaky qwen2.5:3b (the prompt already asked for it; the small model just didn't comply reliably). Fires only with an explicit count ≥ 2; countless/1-commit phrasings defer to the LLM. Combined with the P0 reset fix, M-19 should now fully pass (squash step was always correct).
- **Guardrails:** multi-word / quoted / flag-shaped / non-squash-numeric phrasings (`checkout -b foo`, `branch protection rules`, `show me the last 3 commits`) all defer to the LLM — zero false positives by design. Bare `branch` still lists (read-only).

New tests: `test_canonical_parameterized_branch_and_checkout`, `_squash_count`, `_defers_ambiguous_to_llm`. `cargo test` **198/0**, fmt clean.

**Remaining P2 (LLM-path, needs Ollama up):** M-04 (scope "the login changes" → resolver/multi-select), M-10 (sync→rebase target), M-20 (amend classification stability + clarify-loop convergence). These are prompt/flow work with inherently fuzzy acceptance; deferred to a focused pass.

### ✅ P4 — Redirect drops the original intent — **FIXED** (2026-08-05)

M-13: `commit this` in detached HEAD ran the branch-here rescue, created the branch, then **returned without committing** — the user landed on a new branch believing they'd committed, change still uncommitted.

**Fix (`agent.rs`):** `handle_detached_head_rescue` now returns a `RescueOutcome` (`Resume` | `Done`). Branch-here → `Resume`; the `run_agent` redirect arm falls through to normal intent dispatch on `Resume`, so the original intent actually executes (the commit is made). Switch-away / cancel → `Done` (stop; nothing to resume at the old location). Also routed the branch-name prompt through the gate (`EditableText`, default "rescue-work") instead of a raw `Text::new`, so the rescue is scriptable/testable and non-interactive runs proceed.

New tests: `detached_rescue_branch_here_signals_resume_on_real_branch`, `detached_rescue_switch_away_signals_done`. `cargo test` **200/0**, fmt clean.

### ✅ P3 — Snapshot lifecycle nag — **FIXED** (2026-08-05)

M-08/M-09/M-19/M-21: a paused rebase preserves its snapshot (correct), but after `continue rebase` **completes**, that orphaned snapshot was never cleared — so every later command (even read-only `status`) nagged "interrupted pipeline / run --recover", pointing at a `--recover` that could undo the finished work.

**Fix:** added `RecoveryManager::clear_snapshots_for_workdir` (default method, scoped by workdir). In `execute_pipeline`, when a pipeline that RESOLVED an in-progress op (RebaseContinue/Skip/Abort, MergeAbort, CherryPick/Revert Continue/Abort) completes and `repo.state()` is `Clean`, clear this repo's stale snapshots. Scoped to the workdir so it never touches another repo's live snapshot. New test: `clear_snapshots_for_workdir_removes_only_matching_repo`.

### ✅ P5 — Copy / correctness batch — **FIXED** (2026-08-05)

- **M-08 conflict count "0 file(s)" → real count.** The conflict is written by the `git` subprocess, so the parent's in-memory index was stale → counted 0. Now reloads the index from disk (`index.read(true)`) before counting. Verified end-to-end: `diverged_rebase_conflict_pauses_and_preserves_snapshot` now asserts "in 1 file(s)".
- **M-16 TypeToConfirm wording.** The Reset::Hard safety line hardcoded "type the **branch name**" even when the gate asked for the **commit oid** (undo→discard). Made it token-neutral: "type the highlighted value exactly" — the gate's own `Type 'X' to confirm` line names the exact token.
- **M-12 merge message keeps `# Conflicts:`.** A conflicted `MERGE_MSG` carries a comment block git normally strips at commit; since gitrust reads and commits MERGE_MSG itself, it leaked. Added `strip_comment_lines` (drops `#` lines like git's `core.commentChar`). New test: `test_strip_comment_lines_drops_conflicts_block`.

**State after P0–P5 (offline set complete):** `cargo test` **202/0**, clippy clean (no new lints), fmt clean, release binary rebuilt.

### ✅ P2 LLM-path — **FIXED** (2026-08-07, verified live against Ollama qwen2.5:3b)

The last three high-value failures. **Key finding:** the 3B model cannot be prompted into these — probing showed *identical* reasoning across repeated runs ("push the login changes" → "a push operation") regardless of prompt wording. This matches the SLM literature (small models get little/unreliable benefit from few-shot examples; the fix for *regular, rule-shaped* distinctions is deterministic capture, not prompting). So all three are fixed with **deterministic fast-path capture** — the same research-backed hybrid pattern (deterministic-first, LLM only for genuinely semantic calls) used throughout GiTrust. See [`../../docs`] / the SLM research note.

- **M-04 — FIXED.** `capture_scoped_push` in `intent.rs`: "push [the] `<topic>` changes/files/fixes/work/…" → `FeaturePipeline::AddCommitPush { feature_hint: <topic> }`. Possessive ("my … work"), bare push, and "all/everything" defer to a plain push. Verified live: routes fast-path `*` → the resolver's file-select gate (login = Related, readme = Unrelated/hidden). The *semantic* part (which files are login-related) still runs on the LLM resolver — and works.
- **M-10 — FIXED.** `capture_sync`: "sync with/onto/against `<branch>`" (and "update my branch with …") → `FeaturePipeline::Sync`. Verified live: fast-path `*` → fetch + resolve default branch + Sync plan (was: read-only status). A bare "sync" and "sync check" (fetch-status) correctly excluded.
- **M-20 — FIXED.** `capture_amend_message`: "fix/change/update/reword the [last] commit message to '`<msg>`'" → message-only `Amend`, extracting the quoted/`to:`-delimited new message (case preserved). Verified live: fast-path `*` → amend recognized → **published-commit detection → force-push escalation → `--force-with-lease`** (the full flagship flow that never triggered before).

Redundant M-04 prompt edits reverted to keep the prompt lean (per the research). New tests: `test_canonical_parameterized_sync`, `_scoped_push`, `test_canonical_amend_message_capture`. `cargo test` **205/0**, clippy clean, fmt clean.

### 🎯 State: all P0–P5 + P2-LLM fixed. Remaining is only low-value cosmetic (M-02 glyph alignment, M-06/07 redundant "pull first" nudge, M-03 long-subject re-prompt) — non-blocking for the v0.3.0 gate. Next: bump Cargo.toml → 0.3.0, rebuild, re-run the full M-00…M-30 suite (via runner.sh) targeting 0 FAIL.

---

## Notes carried from the run (keep)
The forensic-recovery subsystem (M-23★★, M-24, M-25, M-28), the trash-net **clean** path (M-26, M-27), divergence reconcile (M-06★, M-07), and the safety guards (M-14★, M-12, M-11) all passed — **do not regress them.** Add them as smoke checks after the fixes land.
