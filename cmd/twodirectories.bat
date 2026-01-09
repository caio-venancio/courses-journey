REM 1. Liste o conteúdo da primeira pasta (sem detalhes, apenas nomes) e salve em um arquivo de texto
dir /b "cmd\tests" > cmd\lista1.txt

REM 2. Faça o mesmo para a segunda pasta
dir /b "cmd\tests2" > cmd\lista2.txt

REM 3. Compare os dois arquivos de lista gerados
fc cmd\lista1.txt cmd\lista2.txt > cmd\comparacao.txt

REM 4. Abra o arquivo comparacao.txt para ver as diferenças. Se estiver vazio, os diretórios são iguais.
