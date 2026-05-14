// this file is used to test debugging using lldb
// non - cmake command:
// 1. clang++ -g -std=c++17 debugger.cpp -o build/prog
// 2. lldb ./build/prog

void func2() {
  int *px = nullptr;
  *px = 2; // dereferencing a nullptr
}

void func1() { func2(); }

int main() {
  func1();
  return 0;
}