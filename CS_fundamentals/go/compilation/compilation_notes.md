# Notes

- GO is a compiled language (like C)
    - GO src code is compile to -> native machine code
    - no interpereter at run time (like python)
    - no VM (like JAVA's JVM which runs java byte code)
    - output is an executable file

- running GO programs => with your terminal & GO file
    (1) run `go run main.go` - [dev-purpose]
    1. GO compiles your code
    2. creates a temporary executable in a temporary dir
    3. runs the executable
    4. deletes the executable

    (2) run `go build main.go` - [deployment-purpose]
    1. after compilation, produces a binary executable `main` or `main.exe`

    (3) multiple files
    - `go run .` or `go build -o my_app .` => build & run packages
    * all must say package main

- go compilation
    go src code -> compiler -> executable
                  (go build)    (./main)
    ```go
    package main
    func main() {
        fmt.Println("Hello world!") // print's a line
    }
    ```
    * executable is platform dependent
        - running go build produces a binary specifically for current OS & CPU architecture
        (i.e. Mac produces darwin executable, with arm64 architecture)
    * but its ez to cross compile
        - for linux (64 bit)
        `GOOS=linux GOARCH=amd64 go build -o myapp-linux main.go`
        `GOOS=windows GOARCH=amd64 go build -o myapp.exe main.go`
        i.e. compiling a dir
        `GOOS=linux GOARCH=amd64 go build -o myapp-linux .` just point it to a folder path instead of the .go file

- go features:
    - compiled => produces an executable
    - static type => checking of types at compile time
        - does seem strongly type (refer to below)
    - easily concurrent
    - has garbage collection
    - fast & lightweight
    - speed: on-par with java

* when doing int * float this err showed up:
./main.go:8:15: invalid operation: costPerMessage * numMessagesFromDoris (mismatched types float64 and int) => seems to me this is a strongly typed language

# -------------------------------------------------------------------------------------------------
# compilation with subdirectories
running go build . only compiles the files in your current directory.
it wont look into subdirectories to find more src files for your current package,
even if they have the same pacakge name at the top!!

# -------------------------------------------------------------------------------------------------
# Initialize a project

1. initialize go project via `go.mod` file

```bash
go mod init <project_name>
```

* `project_name` is just a logical name/ namespace for ur project not a physical folder path reference
    - go knows what to execute & where to find files coz it uses the location of the go.mod file as a physical anchor

2. compile src code

`go build .`

3. run executable

`./<project_name>`

* combine 2 & 3 via `go run .`