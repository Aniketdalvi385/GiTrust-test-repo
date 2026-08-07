# ===== SETUP (M-20) =====
mk_sandbox m20; echo v2 >> app.txt && git commit -qam "typo mesage" && git push -q
# ===== COMMAND (M-20) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-20_scratch/work"
$GITRUST "fix the last commit message to 'typo message fixed'"
