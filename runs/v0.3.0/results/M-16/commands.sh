# ===== SETUP (M-16) =====
mk_sandbox m16; echo "precious content v2" > app.txt && git commit -qam "feat: the mistake"
# ===== COMMAND (M-16) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-16_scratch/work"
$GITRUST "undo"
