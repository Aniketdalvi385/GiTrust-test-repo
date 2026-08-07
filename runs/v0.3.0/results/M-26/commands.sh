# ===== SETUP (M-26) =====
mk_sandbox m26; echo mod >> app.txt; mkdir -p junk/inner && echo tmp > junk/inner/file.txt
# ===== COMMAND (M-26) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-26_scratch/work"
$GITRUST "clean up my repo"
