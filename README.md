# 🔥 sohan-cli (Termux Smart Launcher)

A smart command launcher for Termux that:
- Finds tools/files instantly
- Auto `cd` into directories
- Runs interactive tools safely
- Works with Python & Bash tools

---

## 🚀 Features

- `sohan find file.py` → auto cd + ls
- `sohan camphish` → runs interactive tools safely
- No broken input / no hidden prompts
- Clean zsh integration

---

## 📦 Requirements

- Termux
- zsh
- python

---

## ⚡ Installation (ONE COMMAND)

```bash
git clone https://github.com/sohanhassan407/sohan-cli.git
cd sohan-cli
bash install.sh
```

---

##for installimg zsh

```bash
pkg update -y && pkg upgrade -y
pkg install zsh -y
```
#for make this permanent 
```bash
chsh -s zsh
```