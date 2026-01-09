dir /S /A-D *.* | for /f "delims=" %%i in ('dir /B /A-D *.*') do @echo.%%~xi

@REM dir /B /A-D *.*: Lista recursivamente todos os arquivos (não diretórios) e subdiretórios no formato "bare" (apenas nomes de arquivo).
@REM for %i in (*) do @echo.%~xi: Itera sobre a lista de arquivos e extrai a extensão de cada um. 

