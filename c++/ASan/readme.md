O AddressSanitizer (ASan) é uma ferramenta de detecção de erros de memória rápida para C/C++, integrada ao GCC, Clang e MSVC, que identifica estouros de buffer, use-after-free, leaks e outros problemas de corrupção de memória em tempo de execução. É ativado adicionando -fsanitize=address ao compilar, com baixo impacto no desempenho. 

`gcc -fsanitize=address -o test_asan test_asan.c`