#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main(int argc, char* argv[]) {
  ios_base::sync_with_stdio(false); // de-sync scanf/ printf from cin/ cout
  cin.tie(nullptr);                 // untie cin from cout

  int n;
  cin >> n;
  unordered_map<std::string, int> name_to_count;

  for (auto i{n}; i-- > 0;) {
    std::string curr_name;
    cin >> curr_name;
    auto it = name_to_count.find(curr_name);
    if (it != name_to_count.end()) {
      // exists
      // increment count
      ++it->second;
      // return name with new count
      cout << curr_name << it->second << '\n';
    } else {
      name_to_count[curr_name] = 0;
      cout << "OK" << '\n';
    }
  }
  return 0;
}
