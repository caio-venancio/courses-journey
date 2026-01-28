@echo off
echo [INFO] Usando MinGW do Qt

set "MINGW_BIN=C:\Qt\Tools\mingw1310_64\bin"

set PATH=%MINGW_BIN%;%PATH%

echo gcc:
where gcc
echo mingw32-make:
where mingw32-make

powershell
