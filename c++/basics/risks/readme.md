Embora funcionais, raw pointers são propensos a erros como: 
- [] Memory Leaks: Esquecer de dar delete.
- [] Dangling Pointers: Usar um ponteiro após o delete.
- [] Undefined Behavior: Desreferenciar ponteiros nulos ou não inicializados. 