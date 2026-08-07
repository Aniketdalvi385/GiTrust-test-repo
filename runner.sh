#!/usr/bin/env bash
# runner.sh — capture-only acceptance-suite driver (bash 3.2-compatible).
#
# Division of labor: YOU drive the interactive gates (the judgment steps); CLAUDE
# adjudicates afterward. The runner does all the deterministic work — scaffolds
# runs/vX.Y.Z/, does each test's sandbox setup, runs the command live with the
# terminal ATTACHED (so you make the gate choices and see real output), and
# CAPTURES the full session + post-facts to results/M-NN/output.log. It does NOT
# ask you for a verdict — each record is written PENDING. When you're done, tell
# Claude "adjudicate vX.Y.Z"; Claude reads the output.logs, writes each verdict +
# notes into the per-test README, and generates README.md + REPORT.md.
#
# Usage:
#   ./runner.sh 0.3.0                 # whole suite -> runs/v0.3.0/
#   ./runner.sh 0.3.0 M-05            # a single test
#   ./runner.sh 0.3.0 M-04 M-10 M-20  # a subset, in the given order
#   ./runner.sh 0.3.0 --from M-15     # from M-15 to the end (resume)

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
source "$REPO_ROOT/harness.sh"          # $GITRUST, $TESTROOT, mk_sandbox, mk_teammate, $BR
source "$REPO_ROOT/tests.manifest.sh"   # TEST_ORDER, load_test, t_M_NN functions

# Export the vars a test's live command may reference ($GITRUST "status", etc.),
# so the child shell that runs the command inherits them. Without this, the
# command's literal "$GITRUST" expands to empty in the child and "status" runs as
# a bare command (bash: status: command not found).
export GITRUST TESTROOT REPO_ROOT

# ---- args -------------------------------------------------------------------
VERSION="${1:-}"
if [ -z "$VERSION" ]; then
  echo "usage: $0 <version e.g. 0.3.0> [M-NN ...] | [--from M-NN]" >&2
  exit 2
fi
shift || true

SELECTED=""
if [ "${1:-}" = "--from" ]; then
  start="${2:-}"; seen=0
  for id in $TEST_ORDER; do
    [ "$id" = "$start" ] && seen=1
    [ "$seen" = 1 ] && SELECTED="$SELECTED $id"
  done
elif [ $# -gt 0 ]; then
  SELECTED="$*"
else
  SELECTED="$TEST_ORDER"
fi

RUN_DIR="$REPO_ROOT/runs/v$VERSION"
mkdir -p "$RUN_DIR/results" "$RUN_DIR/evidence"

# ---- colors -----------------------------------------------------------------
if [ -t 1 ]; then
  BOLD=$'\e[1m'; DIM=$'\e[2m'; CYAN=$'\e[36m'; GREEN=$'\e[32m'; RED=$'\e[31m'; YEL=$'\e[33m'; RST=$'\e[0m'
else
  BOLD=""; DIM=""; CYAN=""; GREEN=""; RED=""; YEL=""; RST=""
fi
hr() { printf '%s\n' "${DIM}------------------------------------------------------------${RST}"; }

# ---- version sanity ---------------------------------------------------------
BIN_VER="$("$GITRUST" --version 2>/dev/null | awk '{print $2}')"
n_selected=$(echo $SELECTED | wc -w | tr -d ' ')
echo "${BOLD}GiTrust acceptance runner${RST}  ->  runs/v$VERSION/"
echo "  binary:  $GITRUST"
echo "  version: ${BIN_VER:-<none>}   ${DIM}(run folder: v$VERSION)${RST}"
if [ "$BIN_VER" != "$VERSION" ]; then
  echo "  ${YEL}!  binary --version ($BIN_VER) != run folder ($VERSION). Rebuild + bump Cargo.toml if this run is meant to be v$VERSION.${RST}"
fi
echo "  tests:   $n_selected  ($SELECTED)"
hr

# ---- ollama helpers ---------------------------------------------------------
ollama_running() { pgrep -x ollama >/dev/null 2>&1; }
ensure_ollama() {
  local want="$1"
  if [ "$want" = "off" ] && ollama_running; then
    echo "  ${YEL}This test needs Ollama STOPPED.${RST}  Run:  ${BOLD}brew services stop ollama${RST}"
    read -r -p "  press Enter once Ollama is stopped... " _ </dev/tty
  elif [ "$want" = "on" ] && ! ollama_running; then
    echo "  ${YEL}This test needs Ollama RUNNING.${RST}  Run:  ${BOLD}brew services start ollama${RST}"
    read -r -p "  press Enter once Ollama is up... " _ </dev/tty
  fi
}

# ---- per-test ---------------------------------------------------------------
run_one() {
  local id="$1"
  if ! load_test "$id"; then
    echo "${RED}unknown test: $id${RST}"; return
  fi
  local base="$RUN_DIR/results/$id"
  mkdir -p "$base"
  local log="$base/output.log" cmds="$base/commands.sh"
  : > "$log"; : > "$cmds"

  hr
  echo "${BOLD}${CYAN}$id${RST} - ${BOLD}$T_TITLE${RST}"
  echo "  LLM: $T_LLM   Ollama: $T_OLLAMA"
  [ -n "$T_NOTE" ] && echo "  ${YEL}> $T_NOTE${RST}"
  echo

  ensure_ollama "$T_OLLAMA"

  # Scratch dir for PRE/TIP files; $SBX/work symlinks the test's sandbox work dir.
  export SBX="$TESTROOT/${id}_scratch"
  rm -rf "$SBX"; mkdir -p "$SBX"

  # 1) SETUP — run for the user (subshell so cd/vars don't leak), tee to log.
  if [ -n "$T_SETUP" ]; then
    echo "${DIM}# setup${RST}"
    echo "$T_SETUP" | fold -s -w 76 | sed 's/^/  /'
    { echo "# ===== SETUP ($id) ====="; echo "$T_SETUP"; } >> "$cmds"
    ( eval "$T_SETUP" ) >>"$log" 2>&1
    local rc=$?
    # mk_sandbox <name> uses lowercase, dash-stripped id (m05); link it in.
    local sname; sname="$(echo "$id" | tr 'A-Z' 'a-z' | tr -d '-')"
    if [ -d "$TESTROOT/$sname/work" ]; then
      ln -sfn "$TESTROOT/$sname/work" "$SBX/work"
    fi
    [ $rc -ne 0 ] && echo "  ${YEL}(setup exited $rc - may be expected, e.g. a triggered conflict; see output.log)${RST}"
  fi

  # $BR (the sandbox's branch, e.g. main) is set inside mk_sandbox's subshell and
  # lost when it exits — recover it from the actual sandbox so commands that use
  # "$BR" (checkout $BR, origin/$BR) work. Falls back to main.
  if [ -d "$SBX/work/.git" ] || [ -L "$SBX/work" ]; then
    BR="$(git -C "$SBX/work" symbolic-ref --short HEAD 2>/dev/null || echo main)"
  else
    BR="${BR:-main}"
  fi
  export BR

  # 2) COMMAND — run live with the terminal ATTACHED (you drive the gates),
  # captured via `script`. Runs inside the test's work/ dir when there is one.
  local work_dir="$SBX/work"
  [ -d "$work_dir" ] || work_dir="$REPO_ROOT"
  echo
  echo "${DIM}# live in:${RST} $work_dir"
  echo "  ${BOLD}$T_CMD${RST}"
  echo "  ${YEL}> drive any gates now (arrows/Enter, type-to-confirm, etc.)${RST}"
  { echo "# ===== COMMAND ($id) ====="; echo "cd \"$work_dir\""; echo "$T_CMD"; } >> "$cmds"
  read -r -p "  press Enter to run... " _ </dev/tty
  { echo; echo "# ===== LIVE SESSION ($id) ====="; } >> "$log"
  local sess="$SBX/.session.txt"
  # Source harness.sh inside the child so $GITRUST / $BR / helpers resolve there
  # too (exports cover most, but sourcing is the robust guarantee, and keeps $BR
  # correct for the working dir). Then cd into the test dir and run the command.
  local inner="source \"$REPO_ROOT/harness.sh\" >/dev/null 2>&1; BR=\"$BR\"; cd \"$work_dir\" 2>/dev/null; $T_CMD"
  # Prefer `script` (macOS BSD form: `script [-q] file [command ...]`) so the
  # interactive session is BOTH driveable and captured. If `script` isn't usable
  # (no real tty, unexpected platform), fall back to running the command directly
  # so interactivity is never sacrificed — the transcript is the nice-to-have.
  if command -v script >/dev/null 2>&1 && [ -t 0 ]; then
    script -q "$sess" bash -c "$inner" </dev/tty >/dev/tty 2>&1 || true
    if [ -f "$sess" ]; then
      tr -d '\r' < "$sess" >> "$log"
      rm -f "$sess"
    fi
  else
    echo "  ${DIM}(no tty capture available — running directly; transcript not saved)${RST}"
    bash -c "$inner" </dev/tty >/dev/tty 2>&1 || true
    echo "(session not captured — no tty)" >> "$log"
  fi

  # 3) CHECK — deterministic post-facts, captured for adjudication.
  if [ -n "$T_CHECK" ]; then
    echo
    echo "${DIM}# post-facts (captured for adjudication):${RST}"
    { echo; echo "# ===== POST-FACTS ($id) ====="; } >> "$log"
    ( eval "$T_CHECK" ) 2>&1 | tee -a "$log" | sed 's/^/  /'
  fi

  # 4) CLEANUP
  if [ -n "$T_CLEANUP" ]; then
    ( eval "$T_CLEANUP" ) >/dev/null 2>&1
    echo "  ${DIM}(cleanup ran)${RST}"
  fi

  # 5) CAPTURE ONLY — NO verdict typed here. You drive the gates; the verdict,
  # notes, and per-test README are written by Claude afterward from output.log.
  # A provisional PENDING record is written so the folder + transcript exist.
  write_record "$id" "PENDING" "awaiting adjudication"
  echo
  echo "  ${GREEN}captured${RST} -> results/$id/output.log  ${DIM}(verdict pending — Claude will adjudicate)${RST}"
  printf '%s\tPENDING\t\n' "$id" >> "$RUN_DIR/.verdicts.tsv"
}

write_record() {
  local id="$1" verdict="$2" notes="$3"
  local base="$RUN_DIR/results/$id"
  local glyph
  case "$verdict" in
    PASS) glyph="✅ PASS" ;;
    FAIL) glyph="❌ FAIL" ;;
    PASS-with-defects) glyph="⚠️ PASS (with defects)" ;;
    BLOCKED) glyph="⛔ BLOCKED" ;;
    SKIP) glyph="⏭️ SKIP" ;;
    PENDING) glyph="🕒 PENDING (awaiting adjudication)" ;;
    *) glyph="$verdict" ;;
  esac
  cat > "$base/README.md" <<EOF
# $id · $T_TITLE

| | |
|---|---|
| **LLM** | $T_LLM |
| **Ollama** | $T_OLLAMA |
| **Result** | $glyph |
| **Run** | v$VERSION · $(date '+%Y-%m-%d %H:%M') |

## What to look for
${T_NOTE:-—}

## Command
\`\`\`bash
$T_CMD
\`\`\`

## Notes
${notes:-—}

## Evidence
- [\`commands.sh\`](commands.sh) — setup + command
- [\`output.log\`](output.log) — live session transcript + post-facts
EOF
}

# ---- drive ------------------------------------------------------------------
: > "$RUN_DIR/.verdicts.tsv"
for id in $SELECTED; do
  run_one "$id"
done

# ---- done: hand off to Claude for adjudication ------------------------------
hr
echo "${BOLD}Capture complete - v$VERSION${RST}  (all verdicts PENDING)"
if [ -s "$RUN_DIR/.verdicts.tsv" ]; then
  echo
  awk -F'\t' '{printf "  %-6s %s\n", $1, $2}' "$RUN_DIR/.verdicts.tsv"
fi
echo
echo "  ${DIM}Each test's live transcript + post-facts is saved to"
echo "  runs/v$VERSION/results/M-NN/output.log."
echo
echo "  ${BOLD}Next:${RST} tell Claude \"adjudicate v$VERSION\" (or the ids you ran)."
echo "  ${DIM}Claude reads the output.logs, writes each verdict + notes into the"
echo "  per-test README, then generates README.md + REPORT.md via rollup.sh.${RST}"
