package main // defines an executable program; every GO src file starts with a package declaration => "package mathutils" defines a library

import "fmt" // stands for format; Go's std lib pckg for printing, scanning & string formatting

// any go executable program always needs a main function => entry point for an executable program in like in C
func main() {
	// Sad variable declaration: var style
	var smsSendingLimit int // declares the variable; GO then auto initializes it to the 0 value
	var costPerSMS float64
	var hasPermission bool
	var username string
	fmt.Printf("%v %.2f %v %q\n", smsSendingLimit, costPerSMS, hasPermission, username) // 0 0.00 false ""
	// %v => works for any type
	// %f => float64
	// %.2f => exactly 2 digits after the floating decimal point
	// %q print quoted strings instead of just _ it will be "_"


	// Best way: walrus operator :=
		// declares a new variable & assigns a value to it in 1 line
	my_skill_issues := 42 // will be inferred as an int => type inference!
	// walrus is preferred over var style declarations; only bad thing is that walrus declarations cant be used outside of a funciton (in global/ package scope)

	messageStart := "Happy birthday! You are now"
	age := 21
	messageEnd := "years old!"
	fmt.Println(messageStart, age, messageEnd) // pritns "Happy birthday! You are now 21 years old!"

	/*
	- package main lets the Go compiler know that we want this code to compile and run as a standalone program, as opposed to being a library that's imported by other programs.
	- import "fmt" imports the fmt (formatting) package from the standard library. It allows us to use fmt.Println to print to the console.
	- func main() defines the main function, the entry point for a Go program.
	*/

	/*
	Two Kinds of Errors (in programming):
	1. Compilation errors. Occur when code is compiled. It's generally better to have compilation errors because they'll never accidentally make it into production. You can't ship a program with a compiler error because the resulting executable won't even be created.
	2. Runtime errors. Occur when a program is running. These are generally worse because they can cause your program to crash or behave unexpectedly.
	
	* i.e. compilation err could be wrong syntax causes code to not compile
	* i.e. run time could be doing 1/0 => program was running just that an err happened during runtime
	*/

	/*
	GO's speed 
	generally runs faster than interpreted languages, & compiles faster than other compiled languages => allows for more productive developer experience
	*/

	/*
	signed ints: int  int8  int16  int32  int64
	unsinged ints: uint uint8 uint16 uint32 uint64 uintptr
	signed decimals: float32 float64
	complex numbers: complex64 complex128 => has a real & imaginary part

	* the sizes above represent how many bits in mem will be used to store that variable
	* default int & uint types refer to either 32 or 64 bit sizes depending on the env of the user
	* standard sizes are:
		- int
		- uint
		- float64
		- complex128
	* other default types
		- bool
		- string
		- byte
		- rune
	* straying from default types can make code messy => only use specific types for performance (time & MEM)
	i.e. bad code
	var myAge uint16 = 25
	myAgeInt := int(myAge) // returns the int type => platform dependent so could be 32 or 64
	*/

	// converting types
	temperatureFloat := 88.26
	temperatureInt := int64(temperatureFloat) // casting a float to int => truncates the floating point portion; becomes 88

	mileage, company := 80276, "Toyota" // same as the below 2 lines
	mileage := 80276
	company := "Toyota"

	/*
	GO Run time - run time library that is part of every GO program
	it implements garbage collection, concurrency, stack management & other critical features etc.
	is anagolous to libc (C stadard library)
	* is a small amount of extra code included in the executable binary
	*/

	// constants
	const pi = 3.14159 // can only be primitive types i.e. strings, integers, booleans & floats
	// cant be slices, maps & structs
	// *IMPT: constants must be known at compile time => computation must happen during compile time
	// valid computation
	const firstName = "Lane"
	const lastName = "Wagner"
	const fullName = firstName + " " + lastName // i think, think of it as the compiler doing the actual computation

	// invalid computaitno
	// the current time can only be known when the program is running
	const currentTime = time.Now() // fails computation; valid in JS but not GO

	/*
	Go is generally faster and more lightweight than interpreted or VM-powered languages like:
	- Python
	- JavaScript
	- PHP
	- Ruby
	- Java

	still lgas behind:
	- C
	- C++
	- Rust
	
	* GO is slower due to its automated MEM mgmt aka GO runtime => slower speed but mem safe & simple syntax
	*/

	// *IMPT!! ok lowkey i stopped here since i see that they are just going through all the basic programming language stuff
	// *IMPT!! i did see 1 thing unique about the GO language is channels and that is a specific concept i should pick up

	// writing a function in GO
	
	// params share the same type
	func multiply(x int, y int) int { // return type is after the parantheses
 	   return x * y
	}
	func multiply(x, y int) int {
 	   return x * y
	}
	// no return value
	func logMessage(msg string) {
		fmt.Println(msg)
	}
	// multiple return values
	func divide(a, b float64) (float64, error) {
		if b == 0 {
			return 0, fmt.Errorf("division by zero")
		}
		return a / b, nil
	}
	// using multiple values in GO
	result, _ := divide(10, 2) // if you want to ignore errors
	result, err := divide(10,2)
	result := divide(10,2) // !!THROWS a compile time error!!
	// * take note that this is not a tuple and that its specific that this function then requires 2 variables to store the returned values

	// GO goroutines
	func handleRequests(reqs <-chan request) {
		// changing it to use go routines
		for req := range reqs {
			go handleRequest(req) // go keyword runs the function in a lightweight thread
		}
	}
	// 1. goroutines is a concurrent unit of execution, allowing functions to run concurrently
	// 2. all programs start with main goroutine
	// 3. NOT OS or green threads; coroutines that integrate with GO runtime; rely on GO runtime to suspend them/
	// 4. non preemptive (OS cant force them to context switch, unlike threads)
	// 5. (a) do all goroutines run on 1 thread? NO
	// 	  (b) does each goroutine run on 1 thread? NO
	// 		=> Go uses an (M:N) scheduler, where M # of goroutines multiplex on a much smaller num of N OS threads


}

// variable naming convention in go is to use: camelCase & PascalCase => refers to the Google GO style guide
func otherLearnings() {
	// CONTENT:
	// arrary declaration
	// for loop
	// create dictionary
	// create set

	// --------------------------------------------------------------
	// arrary declaration
	nums := []int {1,2,3,4,5} // compared to C's int arr[n] = {1,2,3}

	// --------------------------------------------------------------
	// for loop
	// both index & val
	for i, v := range nums {
		//smt
	}
	// just index
	for i := range nums {
		//smt nums[i]
	}

	// conceptually: a slice []T always returns 2 values => index && val
	for index, value := range nums {...}
	// for index := range nums {...} // by doing this, u are just ignoring the value & only using the index

	// --------------------------------------------------------------
	// create dictionary
	m := make(map[string]int) // map(keyType)valueType
	m["apple"] = 3
	m["apple"] = 5
	
	// check if key exists
	v, ok := m["apple"]
	if ok {
		fmt.Println(v)
	}
	// declare the dictionary & initialize values tgt
	m := map[string]int{
		"apple":  3,
		"banana": 5,
	}
	
	// --------------------------------------------------------------
	// create set
	// just like creating a dictionary, but the vals are empty
	set := make(map[int]struct{}) // value is struct type
	set[10] = struct{}{}
	set[20] = struct{}{}
	if _, exists := set[10]; exists {
		fmt.Println("10 is in the set")
	}
	delete(set, 10) // to remove the key in the set

	// struct{}{} takes 0 bytes && signals that only keys matter
	// named structs also occupies 0 bytes if it has no fields => MEM occupied depends on fields

	// declaring a named struct (Person in this case)
	type Person struct {
		Name string
		Age int
	}
	// declaring an annoymous struct
	p := struct { // declare
		X int
		Y int
	}{ // & initialize
		X: 10,
		Y: 20,
	}
	// no name, cannt have methods, used for: 1-off data grouping, tests, short lived local structures

	// * GO has no classes!
	// so `struct{}{}` returns an empty annonymous struct
	// nil? XX NO XX => not a type, it represents 0 value for certain type: pointers, maps etc.
	// * there is no 1 liner to convert an "arr" in to a set like in python; idiomatic way is to use for loop

	// --------------------------------------------------------------
	// sorting in go
	sort.Ints(nums) // nums is []int type; func Ints(x []int)

	var a [5]int
	sort.Ints(a) // ❌ compile error
	sort.Ints(a[:]) // must slice it => WORKS

	// other sorting: string, floats, etc.
	sort.Ints([]int)
	sort.Strings([]string)
	sort.Float64s([]float64)

	// custom sorting
	type Person struct {
		Name string
		Age  int
	}

	people := []Person{
		{"Alice", 30},
		{"Bob", 25},
	}

	sort.Slice(people, func(i, j int) bool {
		return people[i].Age < people[j].Age
	})


	// --------------------------------------------------------------
	// slice & array in go
	//array
	var array [5]int
		// fixed size
		// size is part of type => [5]int != [6]int
		// pass by val => entire array is copied
	func f(a [5]int) {
		a[0] = 10 // does NOT affect caller
	}
	
	// slice
	var slice []int // nil cap, len == cap == 0 (no backing array, no allocation) OR s := []int{1,2,3} // slice literal, len == cap == 3
		// dynamic length
		// internally, its a descriptor (struct): pointer, len, capacity
		// passed by value, but points to shared backing array 
	func f(s []int) {
		s[0] = 10 // DOES affect caller
	}

	// * slice's pass by value is passing a copy of the slice header (ptr, len, cap)

	// --------------------------------------------------------------
	// slice (re-slicing & append)
	// re-slicing
	func f(s []int) {
		s = s[:1] // changes local copy only => does not affect the caller
	}
	
	// append
	func f(s []int) {
		s = append(s, 10)
			// checks cap
			// decides where to write
			// MAYBE return a new slice => but it ALWAYS return a slice (new or old)
	}
	// * if len(s) < cap(s), room for append
	// * if len(s) == cap(s), NO room for append; new backing array is allocated

	// length & capacity; IMPT !!
	// (from the above function where 10 is appended to s)
	fmt.Println(len(s)) // 0
	fmt.Println(s)      // []
	// * this is because the length of the declared slice has length 0
	// * when printing out elements of a slice, elements is only printed up till the length (in this case, 0 elements will be printed even though 10 was added to the backing array)
	// ** LENGTH controls visibility, capacity controls groth **

	len(s) // actually this prints out the length of the slice
	s := make([]int, 1, 4)
	len(s) // returns 1, not 0!! => its not the number of elements, its the length allocated to the slice

	// best way to return slices; IMPT !!
	func f(s []int) []int {
		return append(s, 10)
	}
	s = f(s)
	fmt.Println(len(s)) // 1
	fmt.Println(s)      // [10]

	// --------------------------------------------------------------
	// array (append)
	func f(s []int) {
		s = append(s, 99)
		fmt.Println("inside", s)
	}
	s := []int{1,2,3} // slice literal, len == cap == 3
	f(s)
	fmt.Println("outside", s)
	// inside: [1 2 3 99]
	// outside: [1 2 3] => 99 is not displayed as:
		// - append allocates new array
		// - local s within function now points to s
		// - caller's s still points to the old array
		// * impt to note that we are referring to different backing arrays now and not the slices anymore		
}