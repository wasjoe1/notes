#include <cstddef>
#include <stdio.h>
#include <ios>
#include <iostream>
#include <vector>
#include <utility>
#include <tuple>
#include <algorithm>

using namespace std;
using ll = long long;

int main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);

  int n;
  cin >> n;
  int l_width, l_height;
  cin >> l_width >> l_height;

  // create the vector
  vector<tuple<int, int, int>> v;
  v.reserve(n);

  for (auto i{0}; i < n; ++i) {
    int width, height;
    cin >> width >> height;

    // continue if not valid
    if (width <= l_width || height <= l_height) { continue; }

    // place on the vector
    v.emplace_back(width, height, i);
  }

  // sort the vector
  auto comp = [](tuple<int, int, int> x, tuple<int, int, int> y) -> bool {
    // return true for it to be placed infront
    // WRONG
    // if (x[0] != y[0]) { return x[0] < y[0]; }

    // ok: template function resolved at compile time
    // if (get<0>(x) != get<0>(y)) { return get<0>(x) < get<0>(y); }
    
    // structured binding => cleaner
    const auto& [x0, x1, x2] = x; // need const if not its mutable
    const auto &[y0, y1, y2] = y;
    if (x0 != y0) { return x0 < y0; }
    return x1 > y1;
  };
  sort(v.begin(), v.end(), comp); // end() returns the end of the size, not capacity

  // run dp algo on the 2nd part of the array
  vector<int> dp;
  vector<int> indexes;
  vector<int> parents(n, -1); // stores the parent index of the curr_idx
  for (const auto &x : v) {
    const int &curr_val = get<1>(x); // get the current value
    const int &curr_idx = get<2>(x); // get the current index
    // if i can find a slot to place inside the array
    auto it = lower_bound(dp.begin(), dp.end(), curr_val);
    // getting the idx
    // int idx = it - dp.begin();
    int pos = it - dp.begin();
    parents[curr_idx] = pos == 0 ? -1 : indexes[pos-1]; // store the curr_idx: parent_idx

    // modifying without using the idx
    // *it = x.second => think of iterator as a ptr (* operator is probably overloaded)
    if (it == dp.end()) {
      dp.push_back(curr_val);
      indexes.push_back(curr_idx);
    } else {
      *it = curr_val;
      indexes[pos] = curr_idx;
    }
  }

  cout << dp.size() << '\n';

  if (dp.size() < 1) { return 0; }

  // else we want to print all the envelopes, starting from the 2nd dp
  vector<int> chain;
  for (int cur = indexes.back(); cur != -1; cur = parents[cur]) {
    chain.push_back(cur);
  }
  reverse(chain.begin(), chain.end());
  // for (auto i{dp.size()}; i-- > 0;) {}
  for (const auto &x : chain) {
    cout << x+1 << " ";
  }
}


// tests:
// input 1:
// 2 1 1
// 2 2
// 2 2
// output 1:
// 1
// 1

// input 2:
// 3 3 3
// 5 4
// 12 11
// 9 8
// output 2:
// 3
// 1 3 2 
