#include <bits/stdc++.h>
// It is basically a header file that includes every standard library. In programming contests, using this file is a good idea, when you want to reduce the time wasted in doing chores; especially when your rank is time sensitive. 
using namespace std;

int main() {
    vector<int> v = {5, 3, 1, 4, 2};

    // Default ascending order
    sort(v.begin(), v.end());

    for (int i : v) cout << i << " ";
    return 0;
}