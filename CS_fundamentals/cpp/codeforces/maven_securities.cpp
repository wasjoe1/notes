// maven securities example interview qns:
// https://www.mavensecurities.com/revisiting-interview-questions-at-maven/

// - use template metaprogramming to return unique (adjacent) elements in a compile time vector
// - move control flow to compile time via recursive templates for looping

/* Question:
'''Given a vector:
template <int… I> struct Vector;

Assume the vector is sorted. Remove adjacent duplicates from the vector.

For example:

Given: Vector<1, 2, 2, 2, 3, 4, 4, 5>
Produce: Vector<1, 2, 3, 4, 5>

If the vector contains non-adjacent duplicates, it is expected that duplicates will remain

Given: Vector<1, 2, 2, 2, 3, 4, 4, 1, 5>
Produce: Vector<1, 2, 3, 4, 1, 5>

template <typename Vector>
struct uniq
{
   using type = XXX;
};
It is invoked like so: uniq<Vector<1, 2>>::type. It can be verified with
static_assert(std::is_same_v<uniq<Vector<1, 2, 2, 2, 3, 4, 4, 5>>::type, Vector<1, 2, 3, 4, 5>>);

As always, our starting point should be a runtime version of the function so that we understand the control flow that must be converted to runtime:

auto uniq(std::vector<int> const& input)
{
   std::vector<int> output;
   if (!input.empty())
   {
       int previous = input.front();
       output.push_back(previous);
       for (int element : input)
       {
           if (element != previous)
           {
               output.push_back(element);
               previous = element;
           }
       }
   }
   return output;
}
In brief, iterate through the values, and if they do not match the previous last element in the vector then add the new element, otherwise, drop it.
*/
