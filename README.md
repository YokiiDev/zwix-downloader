# Zwix

Simple command-line tool to download videos/audio of **ANY WEBSITE** as MP4 or MP3.

## Requirements

- Python 3.9+
- ffmpeg (required for MP4 and MP3 conversion)

## Quick Start (recommended)

### Windows

1. Put `zwix.py`, `requirements.txt`, and `install_windows.bat` in the same folder.
2. Double-click `install_windows.bat`.
3. It installs the Python packages, offers to install ffmpeg if missing, then launches Zwix.

### Linux

1. Put `zwix.py`, `requirements.txt`, and `install_linux.sh` in the same folder.
2. Make the script executable and run it:

```bash
chmod +x install_linux.sh
./install_linux.sh
```

3. It creates a virtual environment, installs the Python packages inside it, offers to install ffmpeg if missing, then launches Zwix.

## Manual Setup

If you prefer to do it yourself instead of using the install scripts:

### Windows

```bash
python -m pip install --user -r requirements.txt
python zwix.py
```

Make sure ffmpeg is installed and available in your PATH.

### Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 zwix.py
```

Install ffmpeg with your package manager if it is missing, for example:

```bash
sudo apt install ffmpeg
```

## Usage

Once launched, Zwix asks for:

1. **URL** - a YouTube link or a Spotify track link
2. **Format** - `mp4` or `mp3`

Files are saved to:

- Windows: `Desktop/Zwix`
- Linux: `~/zwix`

## Notes

- Spotify links only support MP3 output (audio only), since Zwix resolves the track on YouTube.
- Spotify support works for single tracks only, not playlists or albums.
- No admin/root rights are needed to run Zwix itself. Installing ffmpeg via a system package manager on Linux does require `sudo`.
