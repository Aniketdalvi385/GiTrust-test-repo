# ===== SETUP (M-12) =====
mk_sandbox m12; git checkout -qb side && echo A > app.txt && git commit -qam side; git checkout -q "$BR" && echo B > app.txt && git commit -qam mainline; git merge side >/dev/null 2>&1 || true; echo RESOLVED > app.txt && git add app.txt
# ===== COMMAND (M-12) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-12_scratch/work"
$GITRUST "commit the merge"
