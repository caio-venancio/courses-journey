#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <utility>
#include <limits>
#include <random>
using namespace std;

using Graph = vector<vector<int>>;

Graph createGraph(int n) {
    return Graph(n);
}

void addEdge(Graph &g, int u, int v, bool directed = true) {
    g[u].push_back(v);
    if (!directed) {
        g[v].push_back(u);
    }
}

int main(){
    return 0;
}