// idea: find the largest number out of the 7, then dont negate => add all the
// negated values, then add 2 * largest number found
#include <ios>
#include <iostream>
#include <limits>

using namespace std;

int main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);

  int n;
  cin >> n;

  constexpr size_t k_total = 7;

  for (auto i{n}; i-- > 0;) {
    // set the min number for max_num
    int max_num = std::numeric_limits<int>::min();
    int accum{};
    for (auto j{k_total}; j-- > 0;) {
      int curr;
      cin >> curr;
      // check max num
      max_num = std::max(max_num, curr);
      // add negated val to accum
      accum += (-curr);
    }

    // at the end, add the max number twice
    accum += (2 * max_num);
    cout << accum << '\n';
  }
}