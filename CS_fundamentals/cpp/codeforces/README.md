# Codeforces

# Question Types
_by contest type_
- div 3/ 4 - ~800-2000 rating
- div 2 - ~800-2400 rating, A to F/G qns
- div 1 - higher rated users(1900+)

_by topic (tags)_
- implementation - just correctness, no deep algo required
- greedy - local-choice strategies with proof of correctness??
- DP
- graphs
- data structures
- strings
- binary search
- 2 ptrs / sliding window
- math - number theory, combinatories, probability, modular arithmetic
    - number theory
    - combinatorics
    - geometry
    - constructive algo??
    - game theory

# Compile command

`g++ -std=c++17 -O2 -Wall -Wextra -o main main.cpp`

- `-O2` - optimization level
- `-Wall -Wextra` - catches all warning
- `-o main` - names the ouput executable `main`

# Boiler plate code

```cpp
// WITHOUT EXPLN
#include<bits/stdc++.h>

using namespace std;
using ll = long long;

int main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL); 
}

// WITH EXPLN
#include<bits/stdc++.h> // pulls in entire c++ std lib

using namespace std;

// this is done as alot large edge case numbers cause int to overflow
// easier to do arithmetic calcs in ll
using ll = long long;

int main(int argc, char *argv[]) {
  // unsync cin/cout from C's stdio std lib's scanf/printf
  // cin/cout by default dont get their own indpt internal buffer
  // cin/cout routes every op through the C stdio buffer directly
  // setting sync_with_stdio(false) allows cin/cout to use their own internal buffer (std::streambuf)
  // the thing is, both cin & scanf both still read fd0, but into their own buffers without sync
  // this allows data to be read/write in big chunks, min. sys calls, batch things
  // argc & argv are args used to take in command line arguments
  ios_base::sync_with_stdio(false);

  // by default, cin is tied to cout
  // everytime cin is called `cin >>`, it force flush cout buffer
  // this makes UX nice for interactive programs
  // but for competitive programming, reading from a file/ pipe, wasted calls happen
    cin.tie(NULL);
}
```

# Questions

4a_watermelon.cpp                   800
1a_theatre_square.cpp
71a_way_too_long_words.cpp

282a_bit++.cpp                      800