// CLASS in cpp


// creating class
class Person {
private: // code outside the calss cant access directly
    int age; // age is not shared across the class, every instance has its copy
    static int population; // declaration, shared variable due to static
    static const int x = 5; // constant integral to immediately define variable
    // classes are usually stored in header files & hence these variables are not yet allocated MEM
        // usually treated as a compile-time constant, no MEM is allocated until the variable is actually created at runtime
public:
    static int getPopulation() {
        return population;
    }
}; // its a declaration so need ;

int Person::population = 0; //definition (allowed) => not usage thus it can be accessed
// Person::population = 0; // XX (this not allowed) XX
// why does cpp do this?
// - coz classes are usually placed in header files i.e. Person.h
// - creation of the class is just a definition, not creating the variable yet
// - no MEM allocated yet
// - with line 17, now compiler knows to allocate storage for population variable & initilize to 0

// * access control: private vs public
// instace vs class variables => becomes shared only when use static
    // static variables must be defined outside of the class (no matter whether its private or public)