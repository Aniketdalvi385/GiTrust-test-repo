#!/usr/bin/env bash
# rollup.sh — turn a completed run's per-test records into the version's
# README.md (environment + 31-row index) and REPORT.md (verdict summary).
#
# Run AFTER runner.sh has produced runs/vX.Y.Z/results/M-NN/README.md for the
# tests you ran. Reads each per-test record's Result line (and the session
# ledger .verdicts.tsv if present) and rolls them up.
#
# Usage:  ./rollup.sh 0.3.0

set -uo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
source "$REPO_ROOT/tests.manifest.sh"   # TEST_ORDER, load_test

VERSION="${1:-}"
[ -z "$VERSION" ] && { echo "usage: $0 <version e.g. 0.3.0>" >&2; exit 2; }
RUN_DIR="$REPO_ROOT/runs/v$VERSION"
[ -d "$RUN_DIR/results" ] || { echo "no results in $RUN_DIR — run runner.sh first" >&2; exit 1; }

GITRUST="$(grep '^GITRUST=' "$REPO_ROOT/harness.sh" | head -1 | cut -d= -f2-)"
BIN_VER="$("$GITRUST" --version 2>/dev/null | awk '{print $2}')"

# Pull the recorded Result line out of a per-test README.
verdict_of() {
  local id="$1" f="$RUN_DIR/results/$id/README.md"
  [ -f "$f" ] || { echo "—"; return; }
  grep -E '^\| \*\*Result\*\* \|' "$f" | sed -E 's/^\| \*\*Result\*\* \| (.*) \|$/\1/' | head -1
}
notes_of() {
  local id="$1" f="$RUN_DIR/results/$id/README.md"
  [ -f "$f" ] || return
  awk '/^## Notes$/{getline; if($0!="—") print; exit}' "$f"
}
llm_of() {
  local id="$1" f="$RUN_DIR/results/$id/README.md"
  [ -f "$f" ] || { echo "—"; return; }
  grep -E '^\| \*\*LLM\*\* \|' "$f" | sed -E 's/^\| \*\*LLM\*\* \| (.*) \|$/\1/' | head -1
}
# Title for a row. Base ids (M-04) get it from the manifest; variant sub-ids
# (M-04a) aren't manifest functions, so read the title from the record header
# "# M-04a · <title>".
title_of() {
  local id="$1" f="$RUN_DIR/results/$id/README.md"
  if declare -f "t_$(echo "$id" | tr '-' '_')" >/dev/null 2>&1; then
    load_test "$id" >/dev/null 2>&1; echo "$T_TITLE"; return
  fi
  [ -f "$f" ] && sed -n '1s/^# [^·]*· //p' "$f"
}

# Expand TEST_ORDER into the actual records that exist: a base id with variants
# expands to its present sub-records (M-04 -> M-04a M-04b …); a base id with a
# record of its own stays as-is; ids with neither are skipped. Preserves order.
expand_ids() {
  local base sub found
  for base in $TEST_ORDER; do
    if [ -f "$RUN_DIR/results/$base/README.md" ]; then
      echo "$base"
    fi
    # Append any variant sub-records (base + single letter), in sorted order.
    for sub in "$RUN_DIR/results/$base"?/; do
      [ -d "$sub" ] || continue
      sub="$(basename "$sub")"
      # only accept "<base><letter>", not unrelated dirs
      case "$sub" in
        "$base"[a-z]) echo "$sub" ;;
      esac
    done
  done
}
EFFECTIVE_IDS="$(expand_ids)"

# ---- counts (order matters: match *defect* before the generic *PASS*) -------
pass=0; fail=0; defect=0; blocked=0; skip=0; total=0
for id in $EFFECTIVE_IDS; do
  [ -f "$RUN_DIR/results/$id/README.md" ] || continue
  total=$((total+1))
  v="$(verdict_of "$id")"
  case "$v" in
    *defect*)  defect=$((defect+1));;
    *PASS*)    pass=$((pass+1));;
    *FAIL*)    fail=$((fail+1));;
    *BLOCKED*) blocked=$((blocked+1));;
    *SKIP*)    skip=$((skip+1));;
  esac
done

# ---- README.md (index) ------------------------------------------------------
{
  echo "# GiTrust v$VERSION — acceptance run"
  echo
  echo "| Field | Value |"
  echo "|---|---|"
  echo "| Date | $(date '+%Y-%m-%d') |"
  echo "| OS / arch | $(uname -s) $(uname -m) |"
  echo "| git | $(git --version | awk '{print $3}') |"
  echo "| \`gitrust --version\` | ${BIN_VER:-<none>} |"
  echo "| Ollama model | $(ollama list 2>/dev/null | awk 'NR==2{print $1}') |"
  echo
  echo "**Verdicts:** ✅ $pass PASS · ⚠️ $defect PASS-with-defects · ❌ $fail FAIL · ⛔ $blocked BLOCKED · ⏭️ $skip SKIP"
  echo
  echo "| ID | Title | LLM | Result |"
  echo "|---|---|---|---|"
  for id in $EFFECTIVE_IDS; do
    [ -f "$RUN_DIR/results/$id/README.md" ] || continue
    printf '| [%s](results/%s/) | %s | %s | %s |\n' "$id" "$id" "$(title_of "$id")" "$(llm_of "$id")" "$(verdict_of "$id")"
  done
} > "$RUN_DIR/README.md"

# ---- REPORT.md (summary) ----------------------------------------------------
{
  echo "# GiTrust v$VERSION — Acceptance Report"
  echo
  echo "**Binary:** \`gitrust ${BIN_VER:-?}\` · **Date:** $(date '+%Y-%m-%d') · **Platform:** $(uname -s)/$(uname -m) · **git:** $(git --version | awk '{print $3}')"
  echo
  echo "## Result summary"
  echo
  echo "| Verdict | Count |"
  echo "|---|---|"
  echo "| ✅ PASS | $pass |"
  echo "| ⚠️ PASS with defects | $defect |"
  echo "| ❌ FAIL | $fail |"
  echo "| ⛔ BLOCKED | $blocked |"
  echo "| ⏭️ SKIP | $skip |"
  echo
  echo "## Full results"
  echo
  echo "| ID | Title | Result | Notes |"
  echo "|---|---|---|---|"
  for id in $EFFECTIVE_IDS; do
    [ -f "$RUN_DIR/results/$id/README.md" ] || continue
    printf '| %s | %s | %s | %s |\n' "$id" "$(title_of "$id")" "$(verdict_of "$id")" "$(notes_of "$id")"
  done
  echo
  if [ "$fail" -gt 0 ] || [ "$defect" -gt 0 ]; then
    echo "## Failures & defects to triage"
    echo
    for id in $EFFECTIVE_IDS; do
      [ -f "$RUN_DIR/results/$id/README.md" ] || continue
      v="$(verdict_of "$id")"
      case "$v" in
        *FAIL*|*defect*|*BLOCKED*)
          echo "- **$id** ($(title_of "$id")) — $v — $(notes_of "$id")" ;;
      esac
    done
    echo
  fi
  echo "_Generated by rollup.sh from per-test records in [\`results/\`](results/)._"
} > "$RUN_DIR/REPORT.md"

echo "Wrote:"
echo "  $RUN_DIR/README.md   (environment + $total-test index)"
echo "  $RUN_DIR/REPORT.md   (summary: $pass✅ $defect⚠️ $fail❌ $blocked⛔ $skip⏭️)"
echo
echo "Review them, then add a row to the top-level README Runs table."
