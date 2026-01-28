o que vcpkg install fmt faz?
    O comando vcpkg install fmt baixa, compila e instala a biblioteca de formatação {fmt} (uma alternativa rápida e segura ao printf/iostream) no seu ambiente vcpkg. Ele automatiza a configuração para uso com C++, disponibilizando os arquivos de cabeçalho (include) e bibliotecas (lib) para inclusão direta em projetos. 
    Baixa o código-fonte: Obtém a versão mais recente da biblioteca {fmt}.
    Compila: Compila a biblioteca para o seu compilador e arquitetura (ex: x64-windows).
    Instala: Coloca os arquivos compilados na pasta vcpkg/installed.
    Integração: Torna o {fmt} pronto para ser usado no seu código com #include <fmt/core.h>. 