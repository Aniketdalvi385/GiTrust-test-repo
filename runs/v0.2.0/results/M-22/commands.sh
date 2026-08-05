#!/usr/bin/env bash
# M-22 — Revert parity: succeeds despite the same hook
# Paste the EXACT commands you ran here (so the run is reproducible).
# The harness (GITRUST, TESTROOT, mk_sandbox, mk_teammate, BR) must be sourced first:
#   source ~/GiTrust-test/harness.sh

/Users/aniket.dalvi/Desktop/personal/Glit/gitrust/target/release/gitrust revert last commit 
/Users/aniket.dalvi/Desktop/personal/Glit/gitrust/target/release/gitrust revert last commit 
