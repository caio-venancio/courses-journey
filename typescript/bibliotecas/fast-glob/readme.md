<!-- https://www.npmjs.com/package/fast-glob -->

# O que é?
- https://www.npmjs.com/package/fast-glob
This package provides methods for traversing the file system and returning pathnames that matched a defined set of a specified pattern according to the rules used by the Unix Bash shell with some simplifications, meanwhile results are returned in arbitrary order. Quick, simple, effective

# Como rodar fast-glob em typescript aqui?
npm init -y
npm install fast-glob
npm install --save-dev typescript ts-node
npx ts-node example.ts

# Perguntas
- [X] O que o caminho '**/index.js' faz?
    O padrão **/index.js no fast-glob (uma biblioteca Node.js para encontrar arquivos) é usado para buscar todos os arquivos chamados index.js em qualquer nível de profundidade dentro de um diretório. 
- [X] Qual é o nome dos tipos de padrões que fast-glob aceita?
    O fast-glob utiliza principalmente Glob Patterns (padrões glob) para corresponder a caminhos de arquivos e diretórios, aceitando tanto sintaxe básica quanto avançada. Eles são essencialmente um conjunto de curingas (wildcards) usados no terminal e em linguagens de programação. 
- [] O que é dot true em fast-glob?
    A opção dot: true no fast-glob (e bibliotecas glob baseadas em bash) instrui o correspondente a incluir arquivos e diretórios ocultos (aqueles que começam com um ponto, como .env ou .git) nos resultados da busca. Por padrão, dot é false, o que significa que padrões como * ignoram arquivos ocultos.
- [] Tem como achar pasta com fast-glob?
    Sim, é totalmente possível encontrar pastas utilizando a biblioteca fast-glob no Node.js. Por padrão, o fast-glob foca em encontrar arquivos, mas você pode configurá-lo para retornar apenas diretórios ou arquivos e diretórios combinados. 
- [] O que fg.sync faz?
    O fg.sync do npm package 'fast-glob' é um método síncrono que varre o sistema de arquivos em busca de caminhos que correspondam a padrões definidos (globbing), retornando uma lista de arquivos ou pastas de forma imediata e bloqueante. Ele é ideal para scripts simples de build onde a performance assíncrona não é crítica. 