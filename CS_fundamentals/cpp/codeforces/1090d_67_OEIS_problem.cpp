// #include <bits/stdc++.h>
#include <vector>
#include <iostream>
#include <ios>
#include <cstddef>
#include <cmath>

using namespace std;

// gcd => euclidean algorithm (not really needed actually)
int gcd(int a, int b) {
  // once their ==, means same common divisor
  // when ==, means new_b = a % b = 0, set b to be 0

  // sorting? => actly unnecessary
  //   int bigger = a > b ? a : b;
  //   // b should be smaller
  //   b = bigger == a ? b : a;
  //   a = bigger;

  // 8 % 12 == 8; then new_b is set as 8, a is set as 12

  int new_b;
  while (b != 0) {
    new_b = a % b;
    a = b;
    b = new_b;
  }
  return a;
}

bool is_prime(int curr_num) {
  // need to see if there was any number that curr_num is divisible by
  if (curr_num < 2) { return false; }

  // for (int i{}; pow(i, 2) <= curr_num; ++i) { => WRONG int i cant be 0, else curr_num % 0 is UB!!
  for (int i{2}; pow(i, 2) <= curr_num; ++i) {
    if (curr_num % i == 0) {
      return false; // able to divide by the i value
    }
  }
  return true;
}

vector<int> generate_primes(int n) {
  // TODO: write function that generates n prime numbers
  // vector<int> arr{10}; // list constructor => just 1 element 10
  // vector<int> arr(10); // size constructor => 10 elements all default-initialized with 0
  
  // same example comparision:
  // vector<int> arr{5, 10} // list constructor, 2 elements 5 & 10
  // vector<int> arr(5, 10) // 5 elements all equal to 10

  vector<int> arr;
  if (n == 0) { return arr; }
  arr.reserve(n); // reserves space, but dont initialize elements yet
  // edge case, only need 1 number
  arr.emplace_back(2); // 1 is not prime, hence skipped
  if (n == 1) { return arr; }
  
  int curr_num = 3; // start from 3
  while (arr.size() < n) {
    if (is_prime(curr_num)) {
      // cout << curr_num << endl;
      arr.emplace_back(curr_num);
    }
    curr_num += 2; // always odd number
  }

  return arr; // move semantics
}

ostream& operator<<(ostream &cout, vector<int> arr) {
  // cant take in const ostream& cout => when outputting data via ostream, internal ptrs change, buffer data change etc. CANT be const!
  // cant take in ostream cout => cant copy ostream, can only take in references

  // canonical way to not have trailing ", " => print 1st element, then lead with ", "
  if (arr.empty()) { return cout; } // nothing to print

  cout << arr[0]; // print 1st element
  // for (const auto &x : arr) {
  //   cout << ", " << x;
  // }
  for (size_t i{1}; i < arr.size(); ++i) {
    cout << ", " << arr[i];
  }
  return cout;
}

int old_version_main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);
  // idea: generate the prime numbers, then using prime numbers, generate the
  // sequence of numbers
  // claim 1: we cant use non-prime as gcd numbers (that generate our actual numbers) as those will produce numbers with non-unique gcds
  // claim 2: isPrime only needs to check until the squareroot of X (X being the number to determine isPrime or not)

  // explanation (claim 1): for the entire set of GCD numbers to be truly unique, actual gcd gi has to be
  // gi = gi x gcd(gi-1, gi+1) where gcd(gi-1, gi+1) = 1
  // gcd(gi-1, gi+1) means that the numbers in the set need to be pairwise co-prime => all numbers generated should be prime then

  // explanation (claim 2): to rephrase, if X has any divisors, it would be <= sqrt(x)
  // mathematically, if d divides x, then by defn, x / d = e => every divisor always has a partner e
  // if d > sqrt(x) && e > sqrt(x), then d * e > sqrt(x) * sqrt(x) = x
  // but this is false since d * e = x exactly => hence 1 of them has to be smaller (proof by contradiction)

  // generating prime numbers
  // creating sequence after having the prime numbers
  int n_tests;
  cin >> n_tests;
  // cout << "test: " << n_tests << endl;

  for (int i{n_tests}; i-- > 0;) {
    int n;
    cin >> n;
    vector<int> prime_arr = generate_primes(n-1);
    // cout << "prime number array: " << prime_arr << '\n';
    int prev = 1;
    cout << prev << ' ';
    for (int j{}; j < n-1; ++j) {
      cout << prev * prime_arr[j] << ' ';
      prev = prime_arr[j];
    }
    cout << '\n';
  }
}

vector<long long> create_sequence(const vector<int> &primes) {
  vector<long long> sequence;
  sequence.reserve(primes.size());

  long long prev = 1;
  sequence.emplace_back(prev);

  for (size_t j{}; j < primes.size(); ++j) {
    sequence.emplace_back(prev * primes[j]);
    prev = primes[j]; // implicit casting from int to long long
  }
  return sequence;
}

void print_range(vector<long long> sequence, int n) {
  if (n < 1) { return; }
  cout << sequence[0]; // print the 1st element
  for (int i{1}; i < n; ++i) {
    cout << " " << sequence[i];
  }
}

int main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);

  int n_tests;
  cin >> n_tests;

  // iterate through all the numbers & find the max sequence length
  // generate that max sequence length
  // then run through all again, using the subset of the already generated array
  // to print out all the possible values
  int curr_n{}, max_n{};
  vector<int> all_n;
  all_n.reserve(n_tests);
  for (int i{n_tests}; i-- > 0;) {
    cin >> curr_n;
    max_n = max(max_n, curr_n);
    all_n.emplace_back(curr_n);
  }
  vector<int> prime_arr = generate_primes(max_n - 1);
  vector<long long> max_sequence = create_sequence(prime_arr); // contains 1 + max_n-1

  for (int i{}; i < n_tests; ++i) {
    print_range(max_sequence, all_n[i]);
    cout << '\n';
  }
}