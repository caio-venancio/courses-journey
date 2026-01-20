
Como o VSCode resolve os #include de c++?
    cannot open source file "Inventor/nodes/SoCube.h"C/C++(1696)

Como o cmake resolve os #include de c++?

O que é uma biblioteca que está entre <> em c++?
    Em C++, uma biblioteca ou arquivo de cabeçalho (header file) que está entre colchetes angulares, ou sinais de "menor" e "maior" (< >), no comando #include, é uma biblioteca padrão ou de sistema. 

Como fazer minha própria biblioteca de sistema, que poderá ser usada com <> em cpp?
    Para criar sua própria biblioteca em C++ e usá-la com #include <biblioteca.h> (parênteses angulares), o compilador precisa encontrar os arquivos de cabeçalho (.h ou .hpp) nos diretórios padrão de inclusão do sistema (como /usr/local/include no Linux ou pastas configuradas no seu compilador no Windows). 
    1. Estrutura da Biblioteca
    2. Criar a biblioteca com CMake (CMakeLists.txt) 
    3. Instalar no Sistema
    4. Usar a biblioteca em outro projeto

Como o compilador g++ resolve os #include de c++?
A pasta include existe dentro do g++? Onde ela está no meu sistema?
    Sim, existem pastas de include (arquivos de cabeçalho/headers) utilizadas pelo g++ no seu sistema, mas elas geralmente não ficam "dentro" do executável do g++ em si, e sim em diretórios do sistema configurados durante a instalação do compilador. 

Como encontrar exatamente onde o seu g++ procura?
    g++ -xc++ -E -v -

O que o comando `g++ -xc++ -E -v -` faz exatamente?

Qual a diferença de MinGW e g++?

O que significa linkar manualmente no g++?

O que é um toolchain?

O que é DLL hell?
    DLL Hell (Inferno de DLLs) é um termo que descreve os conflitos e problemas de compatibilidade entre programas no Windows, causados por múltiplas aplicações tentando usar diferentes versões da mesma Biblioteca de Vínculo Dinâmico (DLL), resultando em travamentos, erros ou aplicativos que param de funcionar após a instalação de um novo software, pois um programa sobrescreve a DLL que outro precisa. O problema ocorria porque versões antigas do Windows não gerenciavam bem as dependências, mas foi mitigado com tecnologias como Side-by-Side Assemblies e .NET Framework, que permitem versionamento e empacotamento isolado.

O que é uma biblioteca estática?
    Uma biblioteca estática é um arquivo que contém código de funções e dados compilados, sendo copiada e incorporada diretamente no arquivo executável de um programa durante o tempo de compilação (linking). Isso cria um executável autônomo e independente, que não precisa da biblioteca externa para rodar, mas resulta em arquivos maiores e duplica código se muitos programas usarem a mesma biblioteca, exigindo recompilação para atualizações. 

O que é uma biblioteca dinâmica?
    Uma biblioteca dinâmica é um arquivo com código e dados reutilizáveis que é carregado na memória e vinculado a um programa somente em tempo de execução, não na compilação, permitindo que múltiplos aplicativos compartilhem a mesma cópia, economizando memória e espaço em disco, e facilitando atualizações sem recompilar o executável principal. No Windows, são conhecidas como DLLs (.dll), e em sistemas Unix/Linux como Shared Objects (.so). 

o que é uma biblioteca header-only?
    Uma biblioteca header-only (somente de cabeçalho) é um tipo de biblioteca, comum em C++, onde toda a sua implementação (código-fonte) está contida nos arquivos de cabeçalho (.h ou .hpp), sem necessidade de arquivos .cpp separados, o que significa que não precisa ser compilada e linkada separadamente, bastando incluir os cabeçalhos no projeto e o compilador cuida do resto, sendo fácil de usar, mas podendo aumentar o tempo de compilação e o tamanho do executável. 

Como os sistemas operacionais administram bibliotecas dinâmicas?
    Os sistemas operacionais (SOs) administram bibliotecas dinâmicas — conhecidas como DLLs no Windows (.dll) ou Bibliotecas Compartilhadas no Linux/Unix (.so) — através de um processo chamado vinculação dinâmica (dynamic linking), que adia a resolução de referências de código para o momento da execução (tempo de execução). Isso otimiza o uso de memória e espaço em disco, pois permite que vários programas compartilhem uma única cópia da biblioteca na memória RAM.

O que é essencial um desenvolvedor entender sobre vinculação dinâmica?