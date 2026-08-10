# ===== SETUP (M-10b) =====
mk_sandbox m10b; git remote set-head origin --auto; mk_teammate m10b; git fetch -q; git checkout -qb feature
# ===== COMMAND (M-10b) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-10b_scratch/work"
$GITRUST "update feature from main"
