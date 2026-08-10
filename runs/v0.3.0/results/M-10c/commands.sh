# ===== SETUP (M-10c) =====
mk_sandbox m10c; git remote set-head origin --auto; mk_teammate m10c; git fetch -q; git checkout -qb feature
# ===== COMMAND (M-10c) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-10c_scratch/work"
$GITRUST "pull main into feature"
