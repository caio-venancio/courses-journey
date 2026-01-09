@REM Ele compara o que tem em lista 2 que não tem em lista 1, pelo nomes

REM 1. Liste o conteúdo da primeira pasta (sem detalhes, apenas nomes) e salve em um arquivo de texto
dir /b ".\Windows\cmd\" > Windows\cmd\lista1.txt

REM 2. Faça o mesmo para a segunda pasta
dir /b ".\Windows\powershell\" > Windows\cmd\lista2.txt

REM 3. Compare os dois arquivos de lista gerados
fc cmd\lista1.txt cmd\lista2.txt > cmd\comparacao.txt

REM 4. Abra o arquivo comparacao.txt para ver as diferenças. Se estiver vazio, os diretórios são iguais.
findstr /v /g:Windows\cmd\lista1.txt Windows\cmd\lista2.txt > diferenca_A_B.txt

del Windows\cmd\lista1.txt
del Windows\cmd\lista2.txt