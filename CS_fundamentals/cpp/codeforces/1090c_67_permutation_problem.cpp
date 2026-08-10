#include <bits/stdc++.h>
#include <cstddef>

using namespace std;
using ll = long long;

void permutation(int n) {
  // prints out the permutation here
  // go in 3s
  int total = n * 3;

  for (int i{}; i < n; ++i) {
    int mid_val = total - (2 * i + 1);
    int larger_val = mid_val + 1; // total - 2 * i
    int smaller_val = i + 1;
    cout << smaller_val << ' ' << mid_val << ' ' << larger_val << ' ';
  }
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);

  // code starts here
  int n;
  cin >> n;

  for (int i{}; i < n; ++i) {
    // come up with permutation
    int n_val;
    cin >> n_val;
    permutation(n_val);
    cout << '\n';
  }
}