"""
Zwix v3 - Fast YouTube / Spotify downloader
-----------------------------------------------
- Works on Windows and Linux without admin/root rights
- Downloads video/audio to a local "zwix" folder in the user's home directory
- Supports YouTube links directly and Spotify links (resolved to YouTube via metadata)
- Tuned yt-dlp settings for faster, more parallel downloads
"""

import os
import sys
import time
import shutil
import platform
import requests
import yt_dlp
from pathlib import Path
from pystyle import Colorate, Colors, Center, System

# ---------------------------------------------------------------------------
# UI setup
# ---------------------------------------------------------------------------
System.Title("Zwix v3")

BANNER = """
 ▄▄▄▄▄▄     ▄ ▄   ▄█     ▄
▀   ▄▄▀    █   █  ██ ▀▄   █
 ▄▀▀   ▄▀ █ ▄   █ ██   █ ▀
 ▀▀▀▀▀▀   █  █  █ ▐█  ▄ █
           █ █ █   ▐ █   ▀▄
            ▀ ▀       ▀
"""
BANNER = Colorate.Vertical(Colors.DynamicMIX((Colors.light_blue, Colors.cyan)), Center.XCenter(BANNER))


def clear_screen():
    """Clear the terminal on both Windows and Linux."""
    os.system('cls' if os.name == 'nt' else 'clear')


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
def get_download_path():
    """
    Return the folder where files should be saved, creating it if needed.
    Windows -> Desktop/Zwix
    Linux   -> ~/zwix (i.e. /home/<user>/Zwix-Downloads)
    Using the user's home directory avoids needing root/admin permissions.
    """
    if platform.system() == "Windows":
        download_path = Path.home() / "Desktop" / "Zwix-Downloads"
    else:
        download_path = Path.home() / "zwix"

    download_path.mkdir(parents=True, exist_ok=True)
    return str(download_path)


# ---------------------------------------------------------------------------
# FFmpeg check (no admin/root install performed here - see install scripts)
# ---------------------------------------------------------------------------
def has_ffmpeg():
    """Check whether ffmpeg is available in PATH."""
    return shutil.which("ffmpeg") is not None


# ---------------------------------------------------------------------------
# Spotify support
# ---------------------------------------------------------------------------
def is_spotify_url(url: str) -> bool:
    """Detect whether the given URL points to Spotify."""
    return "open.spotify.com" in url


def get_spotify_track_query(url: str) -> str:
    """
    Resolve a Spotify track URL to a searchable "title artist" string
    using Spotify's public oEmbed endpoint (no API key required).
    Note: this only works for single tracks, not playlists/albums.
    """
    oembed_url = f"https://open.spotify.com/oembed?url={url}"
    response = requests.get(oembed_url, timeout=10)
    response.raise_for_status()
    data = response.json()
    # data["title"] is usually formatted as "Song Name" and the author
    # field sometimes holds the artist name
    title = data.get("title", "")
    author = data.get("author_name", "")
    query = f"{title} {author}".strip()
    if not query:
        raise ValueError("Could not resolve Spotify track metadata.")
    return query


# ---------------------------------------------------------------------------
# Download logic
# ---------------------------------------------------------------------------
def build_ydl_opts(download_path: str, format_choice: str) -> dict:
    """
    Build yt-dlp options tuned for speed:
    - concurrent fragment downloads
    - larger HTTP chunk size
    - sane retry settings
    """
    common_opts = {
        "outtmpl": os.path.join(download_path, "%(title)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "concurrent_fragment_downloads": 8,   # parallel fragment downloads = faster
        "http_chunk_size": 10 * 1024 * 1024,  # 10 MB chunks
        "retries": 10,
        "fragment_retries": 10,
        "socket_timeout": 15,
    }

    if format_choice == "mp4":
        common_opts.update({
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "merge_output_format": "mp4",
        })
    elif format_choice == "mp3":
        common_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })

    return common_opts


def download_video(url: str, format_choice: str):
    """Resolve the source (YouTube/Spotify) and run the download."""
    download_path = get_download_path()

    if format_choice not in ("mp4", "mp3"):
        print(Colorate.Horizontal(Colors.red_to_yellow, "Invalid format!"))
        time.sleep(2)
        clear_screen()
        return main()

    if format_choice == "mp4" and not has_ffmpeg():
        print(Colorate.Horizontal(Colors.red_to_yellow,
                                   "FFmpeg is required for MP4 downloads and was not found."))
        print("Run the install script (install_windows.bat / install_linux.sh) to set it up.")
        time.sleep(3)
        clear_screen()
        return main()

    target = url

    # Spotify only provides audio streams, so we resolve the track name
    # and search for it on YouTube instead of downloading from Spotify directly.
    if is_spotify_url(url):
        try:
            query = get_spotify_track_query(url)
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"Resolved Spotify track: {query}"))
            target = f"ytsearch1:{query}"
            if format_choice == "mp4":
                print(Colorate.Horizontal(Colors.red_to_yellow,
                                           "Spotify links only support MP3, switching format."))
                format_choice = "mp3"
        except Exception:
            print(Colorate.Horizontal(Colors.red_to_yellow, "Could not resolve Spotify link!"))
            time.sleep(3)
            clear_screen()
            return main()

    ydl_opts = build_ydl_opts(download_path, format_choice)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([target])
        print(Colorate.Horizontal(Colors.blue_to_cyan, f"Done! Saved to {download_path}"))
    except Exception:
        print(Colorate.Horizontal(Colors.red_to_yellow, "Download failed! Check the URL and try again."))

    time.sleep(3)
    clear_screen()
    main()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    print(BANNER)
    print(Center.XCenter("V3 | yokiidev"))
    print("")
    url = input(Colorate.Horizontal(Colors.blue_to_cyan, "URL > ")).strip()
    format_choice = input(Colorate.Horizontal(Colors.blue_to_cyan, "Format (MP4/MP3) > ")).strip().lower()
    download_video(url, format_choice)


if __name__ == "__main__":
    main()
