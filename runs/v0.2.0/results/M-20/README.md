# M-20 · Amend-on-pushed: escalation + lease ★

| | |
|---|---|
| **LLM** | yes |
| **Flagship** | ★ |
| **Result** | ❌ FAIL (flaky intent + clarification loop never reaches amend) |
| **Run date** | 2026-08-04 (two runs) |

## What this proves

Lease force-push, no bare --force.

## Procedure

**Setup:**
```bash
mk_sandbox m20
echo v2 >> app.txt && git commit -qam "typo mesage" && git push -q
```

**Steps:**
```bash
$GITRUST "fix the last commit message to 'typo message fixed'"
git rev-parse origin/$BR   # expect == local HEAD after
```

**Expect:** detects the commit is published → escalation explains force-push required → TypeToConfirm on the branch name → remote advances to amended tip, message fixed on remote. **No bare `--force`** anywhere. **★ record.**

## Result

**❌ FAIL — the amend intent was never recognized; the whole flagship force-push-safety flow was unreachable.**

**Setup:** pushed commit `ce35a35 "typo mesage"` (misspelled), local == `origin/main`.

**Request:** *"fix the last commit message to 'typo message fixed'"* — an **amend** of the last commit's message (no new content).

**Actual:** routed as a **new-commit** request, not an amend:
- `gitrust "fix the last commit message to 'typo message fixed'"` (@ llm · ~17.7s) → *"Drafting commit message from diff… ✓"* → drafted **"update files"** (NOT the requested "typo message fixed").
- Then blocked on a pre-check: *"Nothing staged to commit. Stage files first…"* → *"Pre-checks blocked execution."*

So **none** of the four flagship behaviors occurred: no "commit is published" detection, no force-push escalation, no TypeToConfirm on the branch, no `--force-with-lease`. The amend path was never entered.

**Verified nothing changed:**
- Local HEAD still `ce35a35 "typo mesage"`.
- `origin/main` still `ce35a35`; **remote subject still `typo mesage`** (`git log -1 --format=%s origin/main`) — the typo is unfixed. No data loss, but the feature is completely non-functional via this phrasing.

**Two routing-layer defects:**
1. **Amend intent misclassified as new-commit.** "fix the last commit message" should route to amend-message; instead it went to "create a new commit," which then had nothing to commit. Same intent-loss class as M-10 (sync→status).
2. **Quoted argument dropped.** The requested new message *'typo message fixed'* was ignored — it drafted "update files" from the (empty) diff instead of using the user's explicit text. Argument-drop pattern (M-04/05/10), here on the message payload.

**Small positive:** the pre-check correctly **blocked** rather than creating an empty/garbage commit — the "nothing staged" guard did its job, preventing a bad commit. So the failure is clean (blocked), not destructive.

**Could not evaluate** the lease-vs-force assertion, escalation copy, or TypeToConfirm — the flow never reached them. This flagship is blocked upstream by intent routing, independent of whether the amend/force-push machinery itself works.

---

### Second run (same phrasing, for the recording) — CORRECTS the diagnosis

Re-running the identical command produced a **different** (and more informative) failure — the amend intent **was** recognized this time:

- Prompt 1: *"Are you trying to **undo the last commit and change the commit message to 'typo message fixed'**?"* — **correct intent AND correct extracted argument** ('typo message fixed').
- After answering, Prompt 2: *"Do you want to **update the commit message of the last commit to 'typo message fixed'**?"* — again correct.

So the amend path **is reachable** — run 1's misroute-to-new-commit was **LLM non-determinism**, not a hard wall. Diagnosis corrected: amend intent classification is **flaky**, not broken.

**But it still aborted** — a **clarification-loop UX bug**, not the amend logic:
- The flow nested confusing prompts — *"Would you like to provide more context? (no = abort)"* → *"Clarification:"* → *"Do you want to update the commit message…?"* → *"provide more context? (no = abort)"* — and never converged to the amend plan. Answering to proceed just looped back to more clarification; answering "No" aborted.
- On run 2a, leftover pasted text on the input line (`git log -1 --oneline`) was consumed as a prompt answer → *"Invalid answer"* → abort (partly operator paste-timing, but the tool's tight re-prompting made it easy to mis-feed).
- Net: `✗ Aborted` both times; **the escalation / force-push / TypeToConfirm / lease were never reached** because the gate stalls in the clarification loop upstream.

**Verified unchanged (both runs):** local + `origin/main` still `5fd302f "typo mesage"`; remote subject still `typo mesage`. No data loss.

**Revised verdict — still FAIL, revised cause:** the flagship amend-on-pushed flow does not complete. Root causes: (1) **flaky** amend-vs-new-commit classification (run 1 misrouted, run 2 classified correctly), and (2) a **clarification-prompt loop that never converges** to the amend plan (run 2), so the force-push-safety machinery is never exercised. The lease-vs-force assertion remains **unevaluated** — the flow never reaches it.

**Repro:** intent classification is non-deterministic run-to-run; the clarification-loop stall is reproducible once the amend intent IS recognized. Fix phase: stabilize amend classification AND ensure the clarify gate converges to the plan (offer the amend plan directly instead of re-looping "provide more context").

**Notes / evidence:** see [`commands.sh`](commands.sh) and [`output.log`](output.log).
Recording: see [`recording.md`](recording.md).

**On FAIL, record:** what you saw, the exact command, and `git status -sb` at failure.
