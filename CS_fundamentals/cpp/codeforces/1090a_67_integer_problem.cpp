#include <algorithm>
#include <ios>
#include <iostream>

using namespace std;

int main(int argc, char* argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);

  int n ;
  cin >> n;
  for (int i{0}; i < n; ++i) {
    int x;
    cin >> x;
    cout << x << '\n';
  }
}