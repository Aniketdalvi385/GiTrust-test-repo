# ===== SETUP (M-07) =====
mk_sandbox m07; mk_teammate m07; echo "my feature" >> app.txt && git commit -qam "feat: mine" && git fetch -q; git status -sb
# ===== COMMAND (M-07) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-07_scratch/work"
$GITRUST "push"
