# Basic go notes

This file contains some basic syntax of go

# package statement
# PascalCase vs camelCase

# -------------------------------------------------------------------------------------------------
# package statement
`package` statement at the top of a file

- tells the compiler to create an executable, not a library file
- tells the compiler which group of files this file belongs to
- all these files, 1 of them need the package's entry point (i.e. main() function for package main)
    * error occurs if there are 2 functions with the same signature => error, go doesnt support overloading
    * even with different return types, they are considered the same function signature with just the params

* requies this specific signature
func package_name() {...} // no params
i.e.
```go
func main() {} // dont take params
```

* go package is a collection of src files in the same dir that share the same package name
    - all files within the same package can see each other's variables
    - 1 package per dir; every go file in a single dir must have the same package declaration (if this rule broken, compiler fails to compile)
        * error: found package main (file1.go) & side (file2.go) in /path/to/dir

# -------------------------------------------------------------------------------------------------
# PascalCase vs camelCase
- PascalCase -> Exported; means its puvlic & can be accessed by other packages
    * when someone else want to import your package
    i.e. `fmt.Println()` or `http.ListenAndServe()`
- camelCase -> Unexported; private to the package
    * used for internal logic, helper fns, & local variables

# -------------------------------------------------------------------------------------------------
# Immutable Strings

Strings in go are immutable
- 
    ```go
    finalString += string(buffer[:n]) // thus n - 1
    ```
    * this creates a brand new string in memory (allocates new MEM for new string & copy over old string + new string: O(n^2))
- use `strings.Builder` or `bytes.Buffer`
- ```go
    for (i < n) {
        finalString.Write(buffer[:n]) // O(k) where k is length of string being added
    }
    fmt.Println(finalString.String()) // O(n) to "join" the entire string
    ```
