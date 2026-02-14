@echo off
setlocal EnableDelayedExpansion

set "PASTA_A=C:"
set "PASTA_B=G:"

dir /b /s "%PASTA_B%" > listaB_full.txt

:: Extrai só nome dos arquivos da pasta B
(for /f "delims=" %%B in (listaB_full.txt) do @echo %%~nxB) > listaB.txt

set FALTANDO=0

for /r "%PASTA_A%" %%A in (*) do (
    set "ARQ=%%~nxA"
    findstr /x /c:"!ARQ!" listaB.txt >nul
    if errorlevel 1 (
        echo Faltando: !ARQ!
        set /a FALTANDO+=1
    )
)

echo.
echo Total faltando: !FALTANDO!

del listaB_full.txt
del listaB.txt
pause
