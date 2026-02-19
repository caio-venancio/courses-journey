@echo off
setlocal enabledelayedexpansion

set "ROOT=C:"

if not exist "%ROOT%" (
    echo Caminho inválido.
    pause
    exit /b
)

for /d %%D in ("%ROOT%\*") do (
    set "FOLDER_NAME=%%~nxD"
    echo Gerando lista recursiva para %%D

    dir /b /s /a-d "%%D" > "%ROOT%\!FOLDER_NAME!.tmp"

    > "%ROOT%\!FOLDER_NAME!.txt" (
        for /f "usebackq delims=" %%F in ("%ROOT%\!FOLDER_NAME!.tmp") do (
            echo %%~nxF
        )
    )

    del "%ROOT%\!FOLDER_NAME!.tmp"
)

echo Concluído!
pause