# ===== SETUP (M-08) =====
mk_sandbox m08; ( cd "$TESTROOT/m08" && git clone -q remote.git teammate && cd teammate && git config user.email t@test.com && git config user.name teammate && echo "teammate line1" > app.txt && git commit -qam "teammate: app line1" && git push -q ); echo "my line1" > app.txt && git commit -qam "mine: app line1" && git fetch -q; git status -sb
# ===== COMMAND (M-08) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-08_scratch/work"
$GITRUST "push"; echo "EXIT=$?"
