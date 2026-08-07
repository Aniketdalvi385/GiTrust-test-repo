# ===== SETUP (M-19) =====
mk_sandbox m19; echo a > a.txt && git add a.txt && git commit -qm c1; echo b > b.txt && git add b.txt && git commit -qm c2; echo c > c.txt && git add c.txt && git commit -qm c3; git rev-parse "HEAD^{tree}" > "$SBX/TIP.txt"; git rev-list --count HEAD > "$SBX/COUNT.txt"
# ===== COMMAND (M-19) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-19_scratch/work"
$GITRUST "squash the last 3 commits"
