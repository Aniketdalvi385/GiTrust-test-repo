# ===== SETUP (M-14) =====
mk_sandbox m14; git checkout -q "$(git rev-parse HEAD)"; echo y >> app.txt && git commit -qam "detached work"
# ===== COMMAND (M-14) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-14_scratch/work"
$GITRUST "checkout $BR"
