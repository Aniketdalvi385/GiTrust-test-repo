# ===== SETUP (M-11) =====
mk_sandbox m11; ( cd "$TESTROOT/m11" && git clone -q remote.git teammate && cd teammate && git config user.email t@test.com && git config user.name teammate && echo "teammate line1" > app.txt && git commit -qam "teammate: app line1" && git push -q ); echo "my line1" > app.txt && git commit -qam "mine: app line1" && git fetch -q; $GITRUST "push" >/dev/null 2>&1 || true
# ===== COMMAND (M-11) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-11_scratch/work"
$GITRUST "commit my changes"
