#!/usr/bin/env bash

set -e

echo "[+] Installing dependencies..."
pkg update -y
pkg install python zsh eza -y

echo "[+] Creating ~/bin directory..."
mkdir -p ~/bin

echo "[+] Installing sohan.py..."
cp sohan.py ~/bin/sohan.py
chmod +x ~/bin/sohan.py

echo "[+] Updating ~/.zshrc..."

# Backup once
if [ ! -f ~/.zshrc.bak_sohan ]; then
    cp ~/.zshrc ~/.zshrc.bak_sohan 2>/dev/null || true
fi

# Remove old sohan function if exists
sed -i '/^sohan () {/,/^}/d' ~/.zshrc

cat >> ~/.zshrc << 'EOF'

# ───── sohan command ─────
sohan () {

    if [ "$1" = "find" ]; then
        output=$(python ~/bin/sohan.py "$@")

        if echo "$output" | grep -q "^CD:"; then
            dir=$(echo "$output" | grep "^CD:" | cut -d':' -f2-)
            cd "$dir" || return
            echo "$output" | grep -v "^CD:"
            eza --icons
        else
            echo "$output"
        fi
        return
    fi

    python ~/bin/sohan.py "$@"
}

export PATH=$HOME/bin:$PATH
EOF

echo "[+] Done!"
echo "Restart Termux or run: source ~/.zshrc"
