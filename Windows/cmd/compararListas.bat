@echo off
setlocal enabledelayedexpansion

set "FILE1=C:\Users\caiov\Tecnologia da Informacao\Projetos\courses-journey\Windows\cmd\testes\javascript.txt"
set "FILE2=C:\Users\caiov\Tecnologia da Informacao\Projetos\courses-journey\Windows\cmd\testes\c++.txt"

if not exist "%FILE1%" (
    echo Arquivo %FILE1% não encontrado.
    exit /b
)

if not exist "%FILE2%" (
    echo Arquivo %FILE2% não encontrado.
    exit /b
)

set /a TOTAL1=0
set /a TOTAL2=0
set /a IGUAIS=0

rem Conta total lista1
for /f "usebackq delims=" %%A in ("%FILE1%") do (
    set /a TOTAL1+=1
)

rem Conta total lista2
for /f "usebackq delims=" %%A in ("%FILE2%") do (
    set /a TOTAL2+=1
)

rem Conta iguais
for /f "usebackq delims=" %%A in ("%FILE1%") do (
    findstr /x /c:"%%A" "%FILE2%" >nul
    if !errorlevel! == 0 (
        set /a IGUAIS+=1
    )
)

rem Calcula percentual baseado na menor lista
if %TOTAL1% LSS %TOTAL2% (
    set /a BASE=%TOTAL1%
) else (
    set /a BASE=%TOTAL2%
)

if %BASE% EQU 0 (
    set /a PERCENT=0
) else (
    set /a PERCENT=IGUAIS*100/BASE
)

echo -----------------------------
echo Total lista1: %TOTAL1%
echo Total lista2: %TOTAL2%
echo Arquivos iguais: %IGUAIS%
echo Similaridade: %PERCENT%%% 
echo -----------------------------

pause
