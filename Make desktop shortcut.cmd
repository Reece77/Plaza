@echo off
rem Adds a "Plaza" shortcut to your desktop (ported from TST M29). Double-click once.
cd /d "%~dp0"
where uv >nul 2>nul
if errorlevel 1 (
  start "" "%~dp0tools\launcher_missing_uv.html"
  pause
  exit /b 1
)
uv run --project backend python tools\launcher.py --make-shortcut
pause
