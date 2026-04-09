| Algoritmo               | Complexidade     | Estruturas auxiliares  | Ideia do método                            |
| ----------------------- | ---------------- | ---------------------- | ------------------------------------------ |
| Topological Sort (Kahn) | O(V + E)         | fila, array (indegree) | Remove nós com grau de entrada 0           |
| Kosaraju-Sharir         | O(V + E)         | pilha (ou vetor), DFS  | DFS → inverte grafo → DFS na ordem inversa |
| Dijkstra                | O((V + E) log V) | heap (priority queue)  | Expande o menor caminho conhecido          |
| Prim                    | O((V + E) log V) | heap                   | Expande árvore com menor aresta            |
| Kruskal                 | O(E log V)       | Union-Find             | Ordena arestas e evita ciclos              |
