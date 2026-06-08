#include <iostream>
#include <string> // For std::string and std::getline

int main() {
  std::cout << "enter your full name: ";
  std::string name{};
  std::getline(std::cin >> std::ws, name); // read full line of txt into name

  std::cout << "Enter your favourite color: ";
  std::string color{};
  std::getline(std::cin >> std::ws, color);

  std::cout << "your name is " << name << " and your favorite color is "
            << color << '\n';
  return 0;
}