# ===== SETUP (M-30) =====
mkdir -p "$SBX/not_a_repo"
# ===== COMMAND (M-30) =====
cd "/Users/aniket.dalvi/Desktop/personal/GiTrust-test"
cd "$SBX/not_a_repo" && $GITRUST "status"; echo "EXIT=$?"
