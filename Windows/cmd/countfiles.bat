@REM conta quantos arquivos tem no diretório
@REM dir /a-d 
@REM dir /a: O parâmetro de "atributos", que permite filtrar os resultados
@REM dir /a-d: Um modificador para o parâmetro /a. O atributo "d" refere-se a "diretório". O sinal de menos (-) na frente de "d" significa "não" ou "excluir"

dir /a-d | find /c "/"

@REM find /c /v ""
@REM find: O comando principal para procurar texto em arquivos ou na saída de outros comandos.
@REM /v (invert): Mostra todas as linhas que NÃO contêm a string especificada.
@REM /c (count): Conta as linhas que contêm a string e mostra o total, sem exibir as linhas em si.
@REM "" (string vazia): É a "string" que o comando find procura. Como você busca uma string vazia, ele encontra linhas que não são vazias quando usado com /v, ou linhas que são vazias quando usado sem /

@REM dir /a-d | find /c "/"
@REM Desde que dir /a-d retorne apenas as linhas dos arquivos com / nas datas.