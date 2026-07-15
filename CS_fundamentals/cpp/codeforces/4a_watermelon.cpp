#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main(int argc, char* argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL); 
  // w has to be bigger than 2
  // w needs to be even
  int w;
  cin >> w;
  if (w > 2 && w % 2 == 0) {
    cout << "YES";
  } else {
    cout << "NO";
  }
  return 0;
}