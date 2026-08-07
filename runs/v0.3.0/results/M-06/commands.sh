# ===== SETUP (M-06) =====
mk_sandbox m06; mk_teammate m06; echo "my feature" >> app.txt && git commit -qam "feat: mine" && git fetch -q; git status -sb
# ===== COMMAND (M-06) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-06_scratch/work"
$GITRUST "push"
