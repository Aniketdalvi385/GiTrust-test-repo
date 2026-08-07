# ===== SETUP (M-18) =====
mk_sandbox m18; echo a>>app.txt && git commit -qam u1; echo b>>app.txt && git commit -qam u2; echo c>>app.txt && git commit -qam u3; PRE=$(git rev-parse HEAD); echo "PRE=$PRE" > "$SBX/PRE.txt"
# ===== COMMAND (M-18) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-18_scratch/work"
$GITRUST "undo the last 3 commits"
