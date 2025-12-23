#include <bits/stdc++.h>
using namespace std;

int main() {
    vector<int> v = {5, 3, 1, 4, 2};

    // Default ascending order
    sort(v.begin(), v.end());

    for (int i : v) cout << i << " ";
    return 0;
}