// Retornar referências em funções (especialmente em linguagens como C++) é evitado principalmente porque pode levar a referências pendentes (dangling references), resultando em comportamentos indefinidos, travamentos do programa ou corrupção de memória.

// Exemplo de ERRO grave
int& funcaoRuim() {
    int x = 10;
    return x; // O compilador avisa: retornando referencia a local
}
// A referência obtida aqui aponta para "lixo"

// Quando o retorno por referência é aceitável?
// Nem todo retorno por referência é ruim. É seguro retornar uma referência se o objeto referenciado persistir após o término da função, como: 
// Referências a membros de dados (quando bem gerenciado, ex: operator[] em contêineres como std::vector).
// Referências a variáveis estáticas.
// Referências a parâmetros passados por referência para a função. 

// Resumo das Regras
// Nunca retorne uma referência (ou ponteiro) para uma variável local.
// Retorne por valor se o objeto for pequeno ou temporário.
// Use const T& (referência constante) quando quiser evitar cópias de objetos grandes sem permitir modificação. 