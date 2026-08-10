# ===== SETUP (M-20a) =====
mk_sandbox m20a; echo v2 >> app.txt && git commit -qam "typo mesage" && git push -q
# ===== COMMAND (M-20a) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-20a_scratch/work"
$GITRUST "fix the last commit message to 'typo message fixed'"
