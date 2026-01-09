@echo off
SET arquivo1="C:\Users\caiov\Tecnologia da Informação\Projetos\courses-journey\cmd\allfiles.bat"
SET arquivo2="C:\Users\caiov\Tecnologia da Informação\Projetos\courses-journey\cmd\helloworld.bat"

REM Extrai apenas os nomes dos arquivos (incluindo extensões)
FOR %%i IN (%arquivo1%) DO SET nome1=%%~nxi
FOR %%i IN (%arquivo2%) DO SET nome2=%%~nxi

REM Compara os nomes
IF "%nome1%"=="%nome2%" (
    ECHO Os arquivos tem o mesmo nome: %nome1%
) ELSE (
    ECHO Os arquivos tem nomes diferentes: %nome1% vs %nome2%
)