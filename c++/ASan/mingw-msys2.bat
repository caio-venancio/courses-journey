@echo off
echo [INFO] Usando MSYS2 MinGW64

set "MINGW_BIN=C:\msys64\ucrt64\bin"

set PATH=%MINGW_BIN%;%PATH%

echo gcc:
where gcc
echo mingw32-make:
where mingw32-make

powershell