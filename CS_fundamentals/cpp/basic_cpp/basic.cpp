// ------------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------
// std::vector size vs capacity

#include<vector>
#include<iostream>

int main() {
    std::vector<int> v;

    v.size(); // returns number of elements stored in the vector
    v.capacity(); // returns total MEM allocated measured in num of elements it can hold

    std::cout << "size: " << v.size() << "\n";
    std::cout << "size: " << v.capacity() << "\n";
}