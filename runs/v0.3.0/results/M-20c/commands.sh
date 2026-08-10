# ===== SETUP (M-20c) =====
mk_sandbox m20c; echo v2 >> app.txt && git commit -qam "typo mesage" && git push -q
# ===== COMMAND (M-20c) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-20c_scratch/work"
$GITRUST "change my last commit message to 'final wording here'"
