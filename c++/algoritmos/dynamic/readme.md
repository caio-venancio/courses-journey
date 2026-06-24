| Algoritmo                    | Complexidade        | Estruturas auxiliares                  | Ideia do método                                         |
| ---------------------------- | ------------------- | -------------------------------------- | ------------------------------------------------------- |
| Weighted Interval Scheduling | O(n log n)          | Vetor de intervalos, `p(i)`, tabela DP | Escolhe intervalos sem conflito maximizando peso com DP |
| Maior Subsequência Crescente | O(n²) ou O(n log n) | Vetor DP ou busca binária              | Encontra a maior sequência em ordem crescente           |
| Mochila (Knapsack 0/1)       | O(n·W)              | Matriz ou vetor DP                     | Decide incluir ou excluir itens para máximo valor       |
| Menor quantidade de selos    | O(n·V)              | Vetor ou matriz DP                     | Minimiza quantidade de selos para atingir valor         |
| Alinhamento de sequências    | O(m·n)              | Matriz DP                              | Alinha duas sequências maximizando similaridade         |
| Bellman-Ford                 | O(V·E)              | Vetor de distâncias e predecessores    | Relaxa arestas repetidamente e aceita pesos negativos   |
