# ===== SETUP (M-20b) =====
mk_sandbox m20b; echo v2 >> app.txt && git commit -qam "typo mesage" && git push -q
# ===== COMMAND (M-20b) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-20b_scratch/work"
$GITRUST "reword the last commit to 'cleaner subject line'"
