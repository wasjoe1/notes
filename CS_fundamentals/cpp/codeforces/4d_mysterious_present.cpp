#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main(int argc, char* argv[]) {
  // 1st line: longest chain
  // 2nd line: sequence of letters that form the longest chain

  // sort by width then height => if width more than, then i want to sort by
  // height (which ever smaller then strictly comes first)

  // after sorting, check incrementally (if both width and height are < or equal
  // to the prev envelope, then thats the max chain)

  // print the order index by index => data struct: (w, h, idx)
  // 0th index is the envelope
  // 1st index is the 1st envelope

  int n_envelopes;
  cin >> n_envelopes;

  int letter_w, letter_h;
  cin >> letter_w >> letter_h;

  vector<tuple<int, int, int>> arr;
  arr.reserve(n_envelopes);

  for (int i{}; i < n_envelopes; ++i) {
    int w, h;
    cin >> w >> h;
    arr.emplace_back(w, h, i+1);
  }

  sort(arr.begin(), arr.end());

  vector<int> res_arr;
  res_arr.reserve(n_envelopes);

  // int largest_chain = 0;
  for (const auto& [w, h, i] : arr) {
    if (w <= letter_w || h <= letter_h) {
      break; // not valid envelope
    } else {
      // size += 1 // i can just grab the size from below
      // cout << "current printing:" << w << h << i << '\n';
      res_arr.emplace_back(i);
      letter_w = w;
      letter_h = h;
    }
  }
  cout << res_arr.size() << '\n'; // should reflect only the number of idxs that got pushed in
  for (const auto& ele : res_arr) {
    cout << ele << ' ';
  }
  return 0;
}