#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <utility>
#include <limits>
#include <random>
using namespace std;

using Graph = vector<vector<int>>;

vector<int> kahn_topsort(Graph greph){
    int size = greph.size();
    std::vector<int> indegree(size);
    std::vector<int> res;
    //inicializa fila
    std::queue<int> fila;

    //inicializa o indegree de todos
    for (int u = 0; u < size; u++) {
        for (int v : greph[u]) {
            indegree[v]++;
        }
    }

    //adiciona todos os 0 na fila
    for (int u = 0; u < size; u++) {
        if (indegree[u] == 0) {
            fila.push(u);
        }
    }
    //enquanto tiver coisa na fila
    while(!fila.empty()){
        //tira o topo da fila e coloca no resultante
        int top = fila.front();
        fila.pop();
        res.push_back(top);
        //atualiza indegrees e quando der 0 coloca na fila
        for(int v: greph[top]){
            indegree[v]--;
                if(indegree[v] == 0){
                    fila.push(v);
                }
        }
    }
    //se o tamanho de res for menor que o grafo, retorne 0, senão retorna 1
    // verifica ciclo
    if (res.size() != size) {
        return {}; // grafo tem ciclo
    }

    return res;
}

// função auxiliar pra imprimir resultado
void print_result(const vector<int>& res) {
    if (res.empty()) {
        cout << "Tem ciclo!\n";
    } else {
        cout << "Ordem topologica: ";
        for (int x : res) {
            cout << x << " ";
        }
        cout << "\n";
    }
}

int main (){
    cout << "=== Teste 1: DAG simples ===\n";
    Graph g1 = {
        {1, 2}, // 0
        {3},    // 1
        {3},    // 2
        {}      // 3
    };
    print_result(kahn_topsort(g1));

    cout << "\n=== Teste 2: Com ciclo ===\n";
    Graph g2 = {
        {1},
        {2},
        {0} // ciclo
    };
    print_result(kahn_topsort(g2));

    cout << "\n=== Teste 3: Desconexo ===\n";
    Graph g3 = {
        {1},
        {},
        {3},
        {}
    };
    print_result(kahn_topsort(g3));

    cout << "\n=== Teste 4: Um unico nó ===\n";
    Graph g4 = {
        {}
    };
    print_result(kahn_topsort(g4));

    return 0;
}