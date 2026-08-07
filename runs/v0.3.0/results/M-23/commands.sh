# ===== SETUP (M-23) =====
mk_sandbox m23; git checkout -qb experiment && echo "precious work" > precious.txt && git add . && git commit -qm "the work I will lose"; git rev-parse HEAD > "$SBX/LOST.txt"; git checkout -q "$BR" && git branch -D experiment; git rev-parse HEAD > "$SBX/HEADBEFORE.txt"
# ===== COMMAND (M-23) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-23_scratch/work"
$GITRUST "find my lost work"
