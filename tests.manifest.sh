#!/usr/bin/env bash
# tests.manifest.sh — the 31 acceptance tests as data, consumed by runner.sh.
#
# macOS ships bash 3.2 (no associative arrays), so each test is a FUNCTION that
# sets plain variables. The runner calls `load_test M-05`, which dispatches to
# `t_M_05` and populates: T_TITLE T_LLM T_OLLAMA T_SETUP T_CMD T_CHECK T_CLEANUP
# T_NOTE. Empty fields are fine.
#
# Field meaning:
#   T_TITLE    one-line title
#   T_LLM      yes | no | partial | dash   (does it consult the model?)
#   T_OLLAMA   on | off                     (required Ollama state before the test)
#   T_SETUP    shell run in the sandbox BEFORE the gitrust command (may be empty)
#   T_CMD      the command line the runner runs live so YOU drive the gates
#   T_CHECK    shell printing deterministic post-facts (informational only)
#   T_CLEANUP  shell run after the test (chmod back, etc.) — may be empty
#   T_NOTE     reminder printed before the test (what to watch for)
#
# $SBX/work is a symlink to the test's sandbox work/ dir (set by the runner);
# CHECK reads it via `git -C "$SBX/work"`.

# The ordered list of test ids.
TEST_ORDER="M-00 M-01 M-02 M-03 M-04 M-05 M-06 M-07 M-08 M-09 M-10 M-11 M-12 M-13 M-14 M-15 M-16 M-17 M-18 M-19 M-20 M-21 M-22 M-23 M-24 M-25 M-26 M-27 M-28 M-29 M-30"

# Reset all fields, then dispatch to the test's function.
load_test() {
  T_TITLE=""; T_LLM=""; T_OLLAMA="on"; T_SETUP=""; T_CMD=""; T_CHECK=""; T_CLEANUP=""; T_NOTE=""
  local fn="t_$(echo "$1" | tr '-' '_')"
  if ! declare -f "$fn" >/dev/null 2>&1; then
    return 1
  fi
  "$fn"
}

# ============================================================================
# Part 0 — Setup
# ============================================================================
t_M_00() {
  T_TITLE="Build, version, setup"; T_LLM="yes"; T_OLLAMA="on"
  T_CMD='$GITRUST --version'
  T_CHECK='echo "version must match the run folder vX.Y.Z (bump Cargo.toml if not)"'
  T_NOTE='Confirm the release binary is rebuilt and --version matches this run. Optionally run: $GITRUST setup'
}

# ============================================================================
# Part 1 — Everyday operations
# ============================================================================
t_M_01() {
  T_TITLE="Fast-path status (Ollama OFF)"; T_LLM="no"; T_OLLAMA="off"
  T_SETUP='mk_sandbox m01'
  T_CMD='$GITRUST "status"'
  T_CHECK='echo "expect: instant, fast-path marker, NO ollama error"'
  T_NOTE='Ollama must be STOPPED (proves the fast path needs no model).'
}
t_M_02() {
  T_TITLE="LLM-path classification"; T_LLM="yes"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m02'
  T_CMD='$GITRUST "anything new in my repo?"'
  T_CHECK='echo "expect: @ (llm) marker, classified read-only status/log; note latency"'
}
t_M_03() {
  T_TITLE="Commit with editable message"; T_LLM="yes"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m03; echo change >> app.txt'
  T_CMD='$GITRUST "commit this"'
  T_CHECK='git -C "$SBX/work" log -1 --format=%s 2>/dev/null | sed "s/^/HEAD subject: /"'
  T_NOTE='EDIT the draft in the message gate; the commit subject must be YOUR edited text.'
}
t_M_04() {
  T_TITLE="Scoped feature pipeline (flagship)"; T_LLM="yes"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m04; echo "login page" > login.txt; echo "login helper" > auth.txt; echo "unrelated" > readme.txt'
  T_CMD='$GITRUST "push the login changes"'
  T_CHECK='echo "pushed files:"; git -C "$SBX/work" show --stat "origin/$BR" 2>/dev/null | tail -8'
  T_NOTE='PASS = only login.txt + auth.txt committed/pushed; readme.txt must NOT be included.'
}
t_M_05() {
  T_TITLE="Branch create + dirty switch block"; T_LLM="no"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m05'
  T_CMD='$GITRUST "create branch feature-x"; echo x >> app.txt; $GITRUST "checkout $BR"'
  T_CHECK='git -C "$SBX/work" branch -a 2>/dev/null; git -C "$SBX/work" status -sb 2>/dev/null'
  T_NOTE='PASS = feature-x created (fast-path *), then dirty checkout blocked with a clear message (not a crash).'
}

# ============================================================================
# Part 2 — Divergence
# ============================================================================
t_M_06() {
  T_TITLE="Diverged push -> rebase -> clean (flagship)"; T_LLM="yes"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m06; mk_teammate m06; echo "my feature" >> app.txt && git commit -qam "feat: mine" && git fetch -q; git status -sb'
  T_CMD='$GITRUST "push"'
  T_CHECK='echo "left-right vs origin (expect 0 0):"; git -C "$SBX/work" rev-list --left-right --count "origin/$BR...HEAD" 2>/dev/null; git -C "$SBX/work" log --oneline -4 2>/dev/null'
  T_NOTE='At the ChoiceGate read both consequences, then choose REBASE. Flagship - worth recording.'
}
t_M_07() {
  T_TITLE="Diverged -> merge path"; T_LLM="yes"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m07; mk_teammate m07; echo "my feature" >> app.txt && git commit -qam "feat: mine" && git fetch -q; git status -sb'
  T_CMD='$GITRUST "push"'
  T_CHECK='echo "parent count of HEAD (expect 2):"; git -C "$SBX/work" log -1 --format=%P 2>/dev/null | wc -w'
  T_NOTE='At the ChoiceGate choose MERGE.'
}
t_M_08() {
  T_TITLE="Conflicting rebase -> calm pause -> continue (flagship)"; T_LLM="partial"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m08; ( cd "$TESTROOT/m08" && git clone -q remote.git teammate && cd teammate && git config user.email t@test.com && git config user.name teammate && echo "teammate line1" > app.txt && git commit -qam "teammate: app line1" && git push -q ); echo "my line1" > app.txt && git commit -qam "mine: app line1" && git fetch -q; git status -sb'
  T_CMD='$GITRUST "push"; echo "EXIT=$?"'
  T_CHECK='echo "to continue: echo resolved line1 > app.txt && git add app.txt && \$GITRUST \"continue rebase\""'
  T_NOTE='Choose REBASE -> expect CALM pause naming app.txt, nonzero exit, no stack trace. Then run the continue command yourself.'
}
t_M_09() {
  T_TITLE="Abort restores exactly"; T_LLM="no"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m09; ( cd "$TESTROOT/m09" && git clone -q remote.git teammate && cd teammate && git config user.email t@test.com && git config user.name teammate && echo "teammate line1" > app.txt && git commit -qam "teammate: app line1" && git push -q ); echo "my line1" > app.txt && git commit -qam "mine: app line1" && git fetch -q; PRE=$(git rev-parse HEAD); echo "PRE=$PRE" > "$SBX/PRE.txt"; $GITRUST "push" >/dev/null 2>&1 || true'
  T_CMD='$GITRUST "abort rebase"'
  T_CHECK='echo "PRE was: $(cat "$SBX/PRE.txt" 2>/dev/null)"; echo "HEAD now: $(git -C "$SBX/work" rev-parse HEAD 2>/dev/null)"; git -C "$SBX/work" status -sb 2>/dev/null'
  T_NOTE='Setup already triggered the conflict+pause. PASS = HEAD returns to exactly PRE, tree clean, no rebase language.'
}
t_M_10() {
  T_TITLE="Sync with main via origin/HEAD"; T_LLM="yes"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m10; git remote set-head origin --auto; git checkout -qb feature; mk_teammate m10; git fetch -q'
  T_CMD='$GITRUST "sync with main"'
  T_CHECK='echo "does feature now contain the teammate commit?"; git -C "$SBX/work" log --oneline -4 2>/dev/null'
  T_NOTE='Expect target resolved via origin/HEAD -> rebase ChoiceGate -> feature contains mains commit. Choose REBASE.'
}

# ============================================================================
# Part 3 — Stuck states
# ============================================================================
t_M_11() {
  T_TITLE="Mid-rebase never says checkout a branch"; T_LLM="yes"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m11; ( cd "$TESTROOT/m11" && git clone -q remote.git teammate && cd teammate && git config user.email t@test.com && git config user.name teammate && echo "teammate line1" > app.txt && git commit -qam "teammate: app line1" && git push -q ); echo "my line1" > app.txt && git commit -qam "mine: app line1" && git fetch -q; $GITRUST "push" >/dev/null 2>&1 || true'
  T_CMD='$GITRUST "commit my changes"'
  T_CHECK='echo "FAIL instantly if the words \"checkout a branch\" appear"'
  T_NOTE='Setup left the repo mid-rebase. PASS = block names the REBASE + continue/abort verbs. FAIL if it says checkout a branch (S12 regression).'
}
t_M_12() {
  T_TITLE="Merge-aware commit: two parents"; T_LLM="yes"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m12; git checkout -qb side && echo A > app.txt && git commit -qam side; git checkout -q "$BR" && echo B > app.txt && git commit -qam mainline; git merge side >/dev/null 2>&1 || true; echo RESOLVED > app.txt && git add app.txt'
  T_CMD='$GITRUST "commit the merge"'
  T_CHECK='echo "parent count (expect 2):"; git -C "$SBX/work" log -1 --format=%P 2>/dev/null | wc -w; echo "message (must have NO # Conflicts: lines):"; git -C "$SBX/work" log -1 --format=%B 2>/dev/null'
  T_NOTE='PASS = exactly 2 parents AND no "# Conflicts:" lines in the message (M-12 copy fix).'
}
t_M_13() {
  T_TITLE="Detached write -> rescue"; T_LLM="yes"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m13; git checkout -q "$(git rev-parse HEAD)"; echo x >> app.txt'
  T_CMD='$GITRUST "commit this"'
  T_CHECK='echo "branch + did the commit actually happen?"; git -C "$SBX/work" branch 2>/dev/null; git -C "$SBX/work" log -1 --oneline 2>/dev/null; git -C "$SBX/work" status -sb 2>/dev/null'
  T_NOTE='Choose BRANCH-HERE. PASS (post-fix) = branch created AND the commit is actually made (not left uncommitted).'
}
t_M_14() {
  T_TITLE="Stranded-commit guard (flagship)"; T_LLM="no"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m14; git checkout -q "$(git rev-parse HEAD)"; echo y >> app.txt && git commit -qam "detached work"'
  T_CMD='$GITRUST "checkout $BR"'
  T_CHECK='git -C "$SBX/work" branch 2>/dev/null'
  T_NOTE='PASS = guard refuses naive switch, offers branch-here FIRST (commits would be stranded). Take branch-here; commit preserved.'
}

# ============================================================================
# Part 4 — Undo family
# ============================================================================
t_M_15() {
  T_TITLE="Undo gate: four options, names the commit"; T_LLM="no"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m15; echo v2 >> app.txt && git commit -qam "feat: the mistake"'
  T_CMD='$GITRUST "undo"'
  T_CHECK='git -C "$SBX/work" status -sb 2>/dev/null; git -C "$SBX/work" log --oneline -3 2>/dev/null'
  T_NOTE='Expect EXACTLY four options, question names short oid + "feat: the mistake". Choose KEEP STAGED -> commit gone, changes staged.'
}
t_M_16() {
  T_TITLE="Undo -> discard: TypeToConfirm + trash-net"; T_LLM="no"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m16; echo "precious content v2" > app.txt && git commit -qam "feat: the mistake"'
  T_CMD='$GITRUST "undo"'
  T_CHECK='echo "HEAD (commit should be DROPPED post-fix):"; git -C "$SBX/work" log --oneline -3 2>/dev/null; echo "latest trash dirs:"; ls -1t ~/.gitrust/trash/ 2>/dev/null | head -3'
  T_NOTE='Choose DISCARD COMPLETELY -> TypeToConfirm (type the oid). PASS (post-fix) = commit actually dropped; trash backup only if tracked changes existed.'
}
t_M_17() {
  T_TITLE="--yes cannot undo"; T_LLM="no"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m17; echo v2 >> app.txt && git commit -qam "to undo"; PRE=$(git rev-parse HEAD); echo "PRE=$PRE" > "$SBX/PRE.txt"'
  T_CMD='$GITRUST --yes "undo"; echo "EXIT=$?"'
  T_CHECK='echo "PRE: $(cat "$SBX/PRE.txt" 2>/dev/null)"; echo "HEAD: $(git -C "$SBX/work" rev-parse HEAD 2>/dev/null)"'
  T_NOTE='PASS (post-fix) = refusal echoes the gate question (NOT "rebase vs merge"), EXIT=1, HEAD == PRE.'
}
t_M_18() {
  T_TITLE="Multi-count undo halts with guidance"; T_LLM="yes"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m18; echo a>>app.txt && git commit -qam u1; echo b>>app.txt && git commit -qam u2; echo c>>app.txt && git commit -qam u3; PRE=$(git rev-parse HEAD); echo "PRE=$PRE" > "$SBX/PRE.txt"'
  T_CMD='$GITRUST "undo the last 3 commits"'
  T_CHECK='echo "PRE: $(cat "$SBX/PRE.txt" 2>/dev/null)"; echo "HEAD: $(git -C "$SBX/work" rev-parse HEAD 2>/dev/null)"'
  T_NOTE='PASS = no gate, no action; guidance offering squash/revert/undo-most-recent; HEAD unchanged.'
}
t_M_19() {
  T_TITLE="Squash last 3: tree-identical"; T_LLM="yes"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m19; echo a > a.txt && git add a.txt && git commit -qm c1; echo b > b.txt && git add b.txt && git commit -qm c2; echo c > c.txt && git add c.txt && git commit -qm c3; git rev-parse "HEAD^{tree}" > "$SBX/TIP.txt"; git rev-list --count HEAD > "$SBX/COUNT.txt"'
  T_CMD='$GITRUST "squash the last 3 commits"'
  T_CHECK='echo "count before: $(cat "$SBX/COUNT.txt" 2>/dev/null)  after: $(git -C "$SBX/work" rev-list --count HEAD 2>/dev/null)  (expect -2)"; echo "tree before: $(cat "$SBX/TIP.txt" 2>/dev/null)"; echo "tree after:  $(git -C "$SBX/work" rev-parse "HEAD^{tree}" 2>/dev/null)  (expect identical)"'
  T_NOTE='PASS (post-fix) = routes to squash (fast-path), count drops by 2, tree oid identical. Confirm + edit the message.'
}
t_M_20() {
  T_TITLE="Amend-on-pushed: escalation + lease (flagship)"; T_LLM="yes"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m20; echo v2 >> app.txt && git commit -qam "typo mesage" && git push -q'
  T_CMD='$GITRUST "fix the last commit message to '\''typo message fixed'\''"'
  T_CHECK='echo "local HEAD: $(git -C "$SBX/work" rev-parse HEAD 2>/dev/null)"; echo "origin subject: $(git -C "$SBX/work" log -1 --format=%s "origin/$BR" 2>/dev/null)"'
  T_NOTE='Expect published-detection -> force-push escalation -> TypeToConfirm on branch -> --force-with-lease (NO bare --force). Remote subject should become "typo message fixed".'
}

# ============================================================================
# Part 5 — Hook parity
# ============================================================================
t_M_21() {
  T_TITLE="Failing pre-commit blocks (via system git)"; T_LLM="yes"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m21; printf "#!/bin/sh\necho \"LINT FAILED\"; exit 1\n" > .git/hooks/pre-commit; chmod +x .git/hooks/pre-commit; echo x >> app.txt; git rev-list --count HEAD > "$SBX/COUNT.txt"'
  T_CMD='$GITRUST "commit this"; echo "EXIT=$?"'
  T_CHECK='echo "count before: $(cat "$SBX/COUNT.txt" 2>/dev/null)  after: $(git -C "$SBX/work" rev-list --count HEAD 2>/dev/null)  (must be unchanged)"'
  T_NOTE='PASS = hooks-detected info line, commit BLOCKED, "LINT FAILED" surfaced, count unchanged, EXIT nonzero.'
}
t_M_22() {
  T_TITLE="Revert parity: succeeds despite the same hook"; T_LLM="no"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m22; printf "#!/bin/sh\necho \"LINT FAILED\"; exit 1\n" > .git/hooks/pre-commit; chmod +x .git/hooks/pre-commit; echo v2 >> app.txt && git commit -qam "to revert" --no-verify'
  T_CMD='$GITRUST "revert last commit"'
  T_CHECK='git -C "$SBX/work" log --oneline -3 2>/dev/null'
  T_NOTE='PASS = revert SUCCEEDS (inverse commit exists) despite the failing pre-commit. Parity with M-21.'
}

# ============================================================================
# Part 6 — Forensics & trash-net
# ============================================================================
t_M_23() {
  T_TITLE="Deleted branch -> find my lost work (flagship)"; T_LLM="no"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m23; git checkout -qb experiment && echo "precious work" > precious.txt && git add . && git commit -qm "the work I will lose"; git rev-parse HEAD > "$SBX/LOST.txt"; git checkout -q "$BR" && git branch -D experiment; git rev-parse HEAD > "$SBX/HEADBEFORE.txt"'
  T_CMD='$GITRUST "find my lost work"'
  T_CHECK='echo "LOST oid: $(cat "$SBX/LOST.txt" 2>/dev/null)"; echo "HEAD before: $(cat "$SBX/HEADBEFORE.txt" 2>/dev/null)  now: $(git -C "$SBX/work" rev-parse HEAD 2>/dev/null)"; echo "rescue branches (expect one at LOST oid):"; git -C "$SBX/work" branch --list "rescue/*" -v 2>/dev/null'
  T_NOTE='In the RecoveryBrowser pick "the work I will lose". PASS = rescue/* at exactly LOST oid; HEAD untouched. Flagship - record it.'
}
t_M_24() {
  T_TITLE="Dropped stash surfaces"; T_LLM="no"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m24; echo wip >> app.txt; git stash push -m "important wip" >/dev/null 2>&1; git stash drop >/dev/null 2>&1'
  T_CMD='$GITRUST "find my lost work"'
  T_CHECK='git -C "$SBX/work" branch --list "rescue/*" 2>/dev/null'
  T_NOTE='PASS = browser lists a stash-shaped (WIP) candidate; restoring it creates a rescue branch with the wip change.'
}
t_M_25() {
  T_TITLE="Empty-scan honesty"; T_LLM="no"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m25'
  T_CMD='$GITRUST "find my lost work"'
  T_CHECK='echo "expect an honest caveat about never-committed / gc-d work, not a bare nothing-found"'
  T_NOTE='PASS = empty-result message includes the honest unrecoverable caveat.'
}
t_M_26() {
  T_TITLE="Clean-up gate + trash backup, nested dirs"; T_LLM="no"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m26; echo mod >> app.txt; mkdir -p junk/inner && echo tmp > junk/inner/file.txt'
  T_CMD='$GITRUST "clean up my repo"'
  T_CHECK='echo "junk/ removed from tree?"; ls "$SBX/work/junk" 2>/dev/null || echo "  removed"; echo "latest trash backup dir:"; ls -1dt ~/.gitrust/trash/*/ 2>/dev/null | head -1; echo "nested file present in trash?"; ls -1t ~/.gitrust/trash/*/junk/inner/file.txt 2>/dev/null | head -1'
  T_NOTE='Read the gate: it must state tracked/untracked COUNTS + name the trash-net. Choose delete-untracked. Nested file must be byte-identical in trash; tracked mod untouched.'
}
t_M_27() {
  T_TITLE="Fail-closed trash-net"; T_LLM="no"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m27; echo untracked > keepme.txt; mkdir -p ~/.gitrust/trash && chmod 000 ~/.gitrust/trash'
  T_CMD='$GITRUST "clean up my repo"; echo "EXIT=$?"'
  T_CHECK='echo "keepme.txt still present? (must be):"; ls "$SBX/work/keepme.txt" 2>/dev/null && echo "  present"'
  T_CLEANUP='chmod 755 ~/.gitrust/trash 2>/dev/null || true'
  T_NOTE='Choose delete-untracked. PASS = REFUSES (nonzero, names backup failure); keepme.txt still exists. Cleanup restores chmod automatically.'
}
t_M_28() {
  T_TITLE="Recover precedence: sideways pointer"; T_LLM="no"; T_OLLAMA="on"
  T_SETUP='mk_sandbox m28'
  T_CMD='$GITRUST --recover'
  T_CHECK='echo "expect: no interrupted pipeline + pointer to gitrust find my lost work"'
  T_NOTE='PASS = the two recovery worlds introduce each other (sideways pointer present).'
}

# ============================================================================
# Part 7 — Meta
# ============================================================================
t_M_29() {
  T_TITLE="Ollama down: graceful degrade"; T_LLM="dash"; T_OLLAMA="off"
  T_SETUP='mk_sandbox m29'
  T_CMD='$GITRUST "what changed in the auth files?"'
  T_CHECK='echo "then run: \$GITRUST \"status\" (must still work instantly)"'
  T_NOTE='Ollama must be STOPPED. First command should fail friendly (name the fix, no panic); a follow-up status must still work instantly.'
}
t_M_30() {
  T_TITLE="Not a repo"; T_LLM="no"; T_OLLAMA="on"
  T_SETUP='mkdir -p "$SBX/not_a_repo"'
  T_CMD='cd "$SBX/not_a_repo" && $GITRUST "status"; echo "EXIT=$?"'
  T_CHECK='echo "expect: friendly not-a-repo message, no stack trace, EXIT nonzero"'
  T_NOTE='PASS (post-fix) = friendly message AND EXIT=1 (the runner captures gitrust own exit).'
}
