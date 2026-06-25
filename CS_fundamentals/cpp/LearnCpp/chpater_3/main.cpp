#include <iostream>

void print(const std::string &str) {
  std::cout << str;
}

void print_int(int x) {
  std::cout << x << '\n';
}

int main() {
    print("hello world 1\n");
    print("hello world 2\n");
    print("hello world 3\n");
    int x = 4;
    print_int(4);
}