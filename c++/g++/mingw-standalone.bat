@echo off
echo [INFO] Usando MinGW standalone

set "MINGW_BIN=C:\MinGW\bin"

set PATH=%MINGW_BIN%;%PATH%

echo gcc:
where gcc
echo mingw32-make:
where mingw32-make

powershell
