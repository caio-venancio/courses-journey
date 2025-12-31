#include <deque>
#include <iostream>
using namespace std;

int main()
{

    // Declare an empty deque of integers
    deque<int> d1;

    // Declare and initialize a deque with some values
    deque<int> d2 = {10, 20, 30, 40};
    for (int val : d2) {
        cout << val << " ";
    }
    cout << endl;
    return 0;
}