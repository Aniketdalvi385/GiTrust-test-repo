#!/usr/bin/env bash
# Capture helper: tee a command's output into that test's results folder.
# Usage (after sourcing harness.sh):
#   export RUN_DIR=~/GiTrust-test/runs/v0.3.0     # <- the run you're recording into
#   run M-03 $GITRUST "commit this"
#   run M-06 $GITRUST "push"
# It appends to $RUN_DIR/results/<id>/output.log AND echoes the command into
# $RUN_DIR/results/<id>/commands.sh, so both the record and the transcript build up as you go.
# Interactive gates still work (output is teed, not swallowed).
#
# RUN_DIR must point at the current version's run folder. Defaults to the newest runs/* if unset.
: "${RUN_DIR:=$(ls -d "$HOME/GiTrust-test/runs"/*/ 2>/dev/null | sort | tail -1)}"
RUN_DIR="${RUN_DIR%/}"

run() {
  local id="$1"; shift
  if [ -z "${RUN_DIR:-}" ]; then
    echo "run: RUN_DIR is not set — export RUN_DIR=~/GiTrust-test/runs/vX.Y.Z first" >&2
    return 2
  fi
  local base="$RUN_DIR/results/$id"
  mkdir -p "$base"
  # log the command line
  { printf '%s ' "$@"; echo; } >> "$base/commands.sh"
  # header + teed output
  {
    echo "### \$ $*"
  } >> "$base/output.log"
  # run, teeing stdout+stderr to the log while staying interactive
  "$@" 2>&1 | tee -a "$base/output.log"
  local rc=${PIPESTATUS[0]}
  echo "### exit: $rc" >> "$base/output.log"
  echo "(exit $rc)"
  return $rc
}
export -f run 2>/dev/null || true
echo "run() loaded — RUN_DIR=${RUN_DIR:-<unset: export RUN_DIR=~/GiTrust-test/runs/vX.Y.Z>}"
echo "usage: run M-03 \$GITRUST \"commit this\""
