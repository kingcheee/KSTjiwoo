#!/bin/bash
# 모든 프로필에 approvals.mode = off 영구 적용
# 게이트웨이 시작 전에 실행

PROFILES_DIR="/c/Users/sxeyc/AppData/Local/hermes/profiles"
DEFAULT_CONFIG="/c/Users/sxeyc/AppData/Local/hermes/config.yaml"

# default 프로필
if [ -f "$DEFAULT_CONFIG" ]; then
    sed -i 's/approvals:/approvals:/' "$DEFAULT_CONFIG"
    if ! grep -q "mode: off" "$DEFAULT_CONFIG"; then
        sed -i '/approvals:/a\  mode: off' "$DEFAULT_CONFIG"
    fi
    echo "[OK] default 프로필 approvals.mode = off"
fi

# 각 프로필
for profile in "$PROFILES_DIR"/*/; do
    CONFIG="$profile/config.yaml"
    if [ -f "$CONFIG" ]; then
        if ! grep -q "approvals:" "$CONFIG"; then
            echo -e "\napprovals:\n  mode: off" >> "$CONFIG"
        else
            sed -i 's/mode: .*/mode: off/' "$CONFIG"
        fi
        echo "[OK] $(basename "$profile") approvals.mode = off"
    fi
done

echo "완료! 모든 프로필에 approvals.mode = off 적용됨"