#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    vector<char> v = {'a', 'f', 'd'};
  
  	// Inserting 'z' at the back
  	v.push_back('z');
  
  	// Inserting 'c' at index 1
  	v.insert(v.begin() + 1, 'c');

     // Accessing using operator[]
    cout << "Element at index 2 using []: " << v[2] << endl;
    
    // Accessing using at()
    cout << "Element at index 3 using at(): " << v.at(3) << endl;

    // Updating the element at index q
    v[1] = 'c';

    // Finding size
    cout << v.size() << endl;

  	for (int i = 0; i < v.size(); i++)
        cout << v[i] << " ";

    // Deleting last element 'z'
  	v.pop_back();
  
  	// Deleting element 'f'
  	v.erase(find(v.begin(), v.end(), 'f'));

    //simple traversal
    for (int i = 0; i < v.size(); i++)
        cout << v[i] << " ";

    // Add an element
    if(!v.empty()){
        cout<<"Vector is not empty. First element "<<v[0]<<endl;
    }

    return 0;
}