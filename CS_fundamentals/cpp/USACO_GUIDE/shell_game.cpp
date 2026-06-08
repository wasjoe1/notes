#include <iostream> // stdin & stdout is declared as global variables here
#include <vector>

struct Step {
    int a, b, g;
};

int main(int argc, char* argv[]) {
    // argc is always > 0 (at least 1)
    // argv's 1st argument is name or path of the program
    // `std::cin` already ignores leading white space hence it doesnt need
    // `std::ws` when reading multiple texts

    // 3 shells
    // need to simulate where it starts (1 2 or 3)
    // then run the algo each time and check if the swaps are correct

    // set stdin & stdout to shell.in & shell.out
    std::freopen("shell.in", "r", stdin);
    std::freopen("shell.out", "w", stdout);

    int N;
    std::cin >> N;

    std::vector<Step> steps(N); // create N steps
    for (auto i{N}; i-- > 0;) {
        std::cin >> steps[i].a >> steps[i].b >> steps[i].g;
    }

    int max_score{};

    for (auto start_pos{3}; start_pos-- > 0;) {
        int curr_pos{start_pos+1}; // 1-indexed
        int curr_score{};

        for (auto i{N}; i-- > 0;) {
            int a = steps[i].a;
            int b = steps[i].b;
            int g = steps[i].g;

            // do the swap
            if (curr_pos == a || curr_pos == b) {
                curr_pos = curr_pos == a ? b : a;
            }
            // check the result => if correct, add the point
            if (curr_pos == g) { ++curr_score; }
        }
        // check max score
        max_score = std::max(max_score, curr_score);
    }

    std::cout << max_score;
    return 0;
}