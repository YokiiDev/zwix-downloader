#!/bin/bash
# Zwix installer/launcher for Linux
# Installs Python dependencies in user scope and optionally installs ffmpeg.

echo "============================================"
echo "  Zwix Installer - Setting up dependencies"
echo "============================================"
echo

# --- Check python3 is installed -----------------------------------------
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 was not found. Please install it first."
    exit 1
fi

# --- Install Python packages ---------------
echo "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# 3. Installe les dépendances à l'intérieur
echo "Installing Python packages..."
pip install -r requirements.txt

# --- Check ffmpeg ---------------------------------------------------------
if ! command -v ffmpeg &> /dev/null; then
    echo
    read -rp "FFmpeg was not found. Install it now? (y/n): " choice
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        if command -v apt &> /dev/null; then
            sudo apt update && sudo apt install -y ffmpeg
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y ffmpeg
        elif command -v pacman &> /dev/null; then
            sudo pacman -S --noconfirm ffmpeg
        else
            echo "Could not detect a supported package manager. Please install ffmpeg manually."
        fi
    else
        echo "Skipping FFmpeg installation. MP4/MP3 conversion may fail without it."
    fi
else
    echo "FFmpeg already installed, skipping."
fi

echo
echo "Setup complete! Launching Zwix..."
echo
python3 zwix.py
