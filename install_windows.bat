@echo off
setlocal enabledelayedexpansion
title Zwix Installer

echo ============================================
echo   Zwix Installer - Setting up dependencies
echo ============================================
echo.

:: --- Check Python is installed ---------------------------------------
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python was not found in PATH. Please install Python 3.9+ first.
    pause
    exit /b 1
)

:: --- Install Python packages (user scope, no admin needed) ------------
echo Installing Python packages...
python -m pip install --user -r requirements.txt

:: --- Check FFmpeg -------------------------------------------------------
where ffmpeg >nul 2>nul
if errorlevel 1 (
    echo.
    echo FFmpeg was not found on your system.
    set /p INSTALL_FFMPEG="Do you want to install FFmpeg now? (Y/N): "
    if /i "!INSTALL_FFMPEG!"=="Y" (
        echo Downloading FFmpeg to a local user folder, no admin rights required...
        set "FFMPEG_DIR=%LOCALAPPDATA%\Zwix\ffmpeg"
        mkdir "!FFMPEG_DIR!" 2>nul

        powershell -NoProfile -Command "Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile '%TEMP%\ffmpeg.zip'"
        powershell -NoProfile -Command "Expand-Archive -Path '%TEMP%\ffmpeg.zip' -DestinationPath '!FFMPEG_DIR!' -Force"

        for /d %%d in ("!FFMPEG_DIR!\ffmpeg-*") do set "FFMPEG_BIN=%%d\bin"

        :: Add ffmpeg to the USER PATH only (does not require admin rights)
        setx PATH "%PATH%;!FFMPEG_BIN!" >nul

        echo FFmpeg installed to !FFMPEG_BIN! and added to your user PATH.
        echo Please close and reopen this terminal for the change to take effect,
        echo then run this script again.
        pause
        exit /b 0
    ) else (
        echo Skipping FFmpeg installation. MP4/MP3 conversion may fail without it.
    )
) else (
    echo FFmpeg already installed, skipping.
)

echo.
echo Setup complete! Launching Zwix...
echo.
python zwix.py
pause
