@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
SET "ext_list="
(
    FOR /F "tokens=*" %%F in ('DIR /B /S /A:-D *.*') DO (
        REM Extrai a extensão do nome do arquivo (inclui o ponto)
        SET "current_ext=%%~xF"
        REM Verifica se a extensão já está na lista
        IF "!ext_list! :!current_ext!" NEQ "!ext_list!" (
            REM Se for nova, adiciona à lista e imprime (ou redireciona para um arquivo)
            SET "ext_list=!ext_list! :!current_ext!"
            ECHO !current_ext!
        )
    )
)> lista_de_extensoes.txt
REM O comando acima redireciona a saída (ECHO) para um arquivo chamado lista_de_extensoes.txt
REM Opcional: Classificar o arquivo de saída
SORT lista_de_extensoes.txt /O lista_de_extensoes_ordenada.txt
DEL lista_de_extensoes.txt
ENDLOCAL
PAUSE