# ===== SETUP (M-27) =====
mk_sandbox m27; echo untracked > keepme.txt; mkdir -p ~/.gitrust/trash && chmod 000 ~/.gitrust/trash
# ===== COMMAND (M-27) =====
cd "/var/folders/s7/1jv371kn3l94rpcf9w_3dy740000gp/T//gitrust-sandboxes/M-27_scratch/work"
$GITRUST "clean up my repo"; echo "EXIT=$?"
