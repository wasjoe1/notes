#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main(int argc, char* argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  // idea is that peter can study as much as he wants
  // find min time he can study
  // find max time he can study
  // if time that parent wants him to study is within this bounds,
    // it means that he can study that amount of hours

  // since we need a solution, we first use the min numbers for each output
  // then add the difference of the curr element, to each min. element, until
  // the difference creates an exceed

  int d, sum_time;
  cin >> d >> sum_time;

  vector<int> min_time_arr, max_time_arr;
  min_time_arr.reserve(d);
  max_time_arr.reserve(d); // this just reserves capacity()
  
  int max_hours{};
  int min_hours{};

  for (int i = 0; i < d; ++i) {
    int a, b;
    cin >> a >> b;
    min_time_arr.emplace_back(a); // emplace back actually increases size()
    max_time_arr.emplace_back(b);
    max_hours += max_time_arr[i];
    min_hours += min_time_arr[i];
  }

  if (sum_time < min_hours || sum_time > max_hours) {
    cout << "NO";
    return 0;
  } else {
    cout << "YES\n";
  }

  // if yes need to find 2 numbers
  int i{};
  for (; i < d; ++i) {
    // else we still need to continue adding
    min_hours += (max_time_arr[i] - min_time_arr[i]);
    // if its too big, we want to break
    if (min_hours >= sum_time) {
      break;
    }
    // else we just print it out
    cout << max_time_arr[i] << ' ';
  }
  // TEST
  // cout << i << "last idx value"; // i == d when for loop fully runs

  // if it was broken, we need to start from not yet printed i
  if (i < d) {
    min_hours -= (max_time_arr[i] - min_time_arr[i]); // revert min_hours first
    cout << min_time_arr[i] + (sum_time - min_hours) << ' ';
    i += 1;

    // complete the rest of the loop
    for (; i < d; ++i) {
      cout << min_time_arr[i] << ' ';
    }
  }

  return 0;
}