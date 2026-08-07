# ===== SETUP (M-09) =====
mk_sandbox m09; ( cd "$TESTROOT/m09" && git clone -q remote.git teammate && cd teammate && git config user.email t@test.com && git config user.name teammate && echo "teammate line1" > app.txt && git commit -qam "teammate: app line1" && git push -q ); echo "my line1" > app.txt && git commit -qam "mine: app line1" && git fetch -q; PRE=$(git rev-parse HEAD); echo "PRE=$PRE" > "$SBX/PRE.txt"; $GITRUST "push" >/dev/null 2>&1 || true
# ===== COMMAND (M-09) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-09_scratch/work"
$GITRUST "abort rebase"
