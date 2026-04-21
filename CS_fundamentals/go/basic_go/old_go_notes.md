# Notes

## why do we need to init go modules?
## fmt.Fprintln vs fmt.Println
## GO does not have F-string literals like python
## slice
## printing to stdout (concatenation & format)
## state machine
## io.ReadCloser
## Channels
## IIFE
## Error handling in GO
## TCP
## Goroutine
## net.Conn & io.ReadCloser interfaces
## log vs fmt
## Miscellaneous Notes/ Fun Facts
## boot.dev cli installation

# -------------------------------------------------------------------------------------------------
## why do we need to init go modules?
1. define the module's identity
2. manage dependencies for project
3. module context required to handle imports & integrate with GO toolchain features

# -------------------------------------------------------------------------------------------------
## fmt.Fprintln vs fmt.Println
    fmt.Println("hello") => always prints to stdout `fd 0, 1 & 2 are for stdin, stdout & stderr by default opened by the OS`
    fmt.Fprintln(os.Stderr, "error:", err) => takes in any io.Writer, & the rest of the params are string args where a single space is inserted between them `func Fprintln(w io.Writer, a ...any) (n int, err error)`

# -------------------------------------------------------------------------------------------------
## GO does not have F-string literals like python
    - From fastest → slowest:
        1. strings.Builder
        2. string + strconv
        3. fmt.Sprint
        4. fmt.Sprintf
    - string rules of thumb
        Debug / logs → fmt.Sprintf
        Fast paths → concatenation or strings.Builder
        Large strings → strings.Builder

# -------------------------------------------------------------------------------------------------        One-off prints → fmt.Println / fmt.Printf
## slice
    - not an array
    - is a view over an array => *UTH its implemented using a struct with the fields: data, length, capacity
        - data (or ptr) - a ptr to the first element of the underlying array that the slice can access
        - len - # of elements accessible in the slice
        - cap - max # of ele that underlying array can hold
    - i.e. `make([]T, len, cap)` => when only 1 size is speicified `make([]T, size)` len == cap
    ```go
    type slice struct {
        ptr *T
        len int
        cap int
    }

# -------------------------------------------------------------------------------------------------    ```
## printing to stdout (concatenation & format)
    format: * use fmt.printf when printing to stdout => format strings %s, %v etc.
	concatenation: * & fmt.Println => insert space betwn args, & \n char at concatenationend
*UTH - under the hood

# -------------------------------------------------------------------------------------------------
## state machine
defn: A state machine is a mathematical abstraction used to design algorithms.
basically reads a set of inputs and changes to a different state, based on those inputs.
https://developer.mozilla.org/en-US/docs/Glossary/State_machine

# -------------------------------------------------------------------------------------------------
## io.ReadCloser
it is an interface from the GO standard library
```go
type ReadCloser interface {
    Read(p []byte) (n int, err error)
    Close() error
}
```

# -------------------------------------------------------------------------------------------------
## Channels
`chan string` => send & receive channel, carries string type data
`<- chan string` => receive only channel, carries string type data; cant insert values to channel
    allowed action: value := <- ch // blocks until value is able to receive
`chan <- string` => send only channel, carries string type data; cant retrieve values from the channel
    allowed action: ch <- value // send value to ch; blocks until the other side is ready to receive

- unbuffered channels
ch := make(chan string)
Capacity = 0
ch <- value
* this means blocks until a receiver is ready, at most 1 value is stored (MEM usage constant)

- Buffered channel
ch := make(chan string, 16)
Capacity = 16
Holds at most 16 strings => bounded memory with a small queue

- []string ?
why []string cant be used? wouldnt the exercise where we ingest data by chunks show that we can use string arrays initially and chunk them to not overrun the MEM?
No.
looking at this function `func getLines(f io.ReadCloser) []string`
this means the entire string needs to be read into MEM
whereas if we do `func getLines(f io.ReadCloser) <-chan string` the content can be buffered inside the channel first & block the socket from continuing to send us data

- how to add data into receive-only channel & vice versa
chanel types are interpreted by the caller of the function, not inside the function it was created
```go 
func getLinesChannel(f io.ReadCloser) <-chan string {
    ch := make(chan string) // channel creation, currently its bi directional
        // you can send (ch <- value)
        // you can receive (val := <-ch)
        // you can close it 
    value := 3
    ch <- value
    return ch // GO implicitly converts `chan string` to `<-chan string`
}
```

# -------------------------------------------------------------------------------------------------
## IIFE
```go
// this defines an annonymous function and immediately executes it asynchronously
go func() {
    ...
}()   // ← call
```
pattern is called an IIFE (Immediately Invoked Function Expression)

# -------------------------------------------------------------------------------------------------
## Error handling in GO
```go
// idiomatic way to handle error
v, err := doThing()
if err != nil {
    return err
}

// i.e. common example in servers/ sockets
conn, err := net.Dial("tcp", addr)
if err != nil {
    return fmt.Errorf("dial %s: %w", addr, err)
}
defer conn.Close() // since the conn is now open, we have to defer the closing b4 this func ends

// checking for exact error
if errors.Is(err, context.DeadlineExceeded) {
    // map to 504, retry, etc.
}
```
This may come as a surprise but GO does not have a try catch block to handle errors.
It relies on developers to __explicitly__ handle errors. it forces devs to think if they should
immediately handle the error within this block, of raise it up an abstraction layer (in larger code bases).
e.g.
```python
try {
    a()
    b()
    c()
} catch (Exception e) {
    handle(e) # here you cant tell which error u are actually handling
}
```
```go
if err := a(); err != nil { return err } // whereas here, u are able to see exactly which function throws an error
if err := b(); err != nil { return err }
if err := c(); err != nil { return err }
```

# -------------------------------------------------------------------------------------------------
## TCP
recap TCP from the course:
- ordered; udp could be unordered
- connection oriented, 3 way handshake; udp isnt

# -------------------------------------------------------------------------------------------------
## Goroutine
Goroutine work using M:P:G scheduling model != does not use a single event loop (like in python)
Go runtime has a scheduler that multiplexes Goroutines(G) on to a small number of OS threads(M),
managed by a pool of logical processors(Ps)

Go scheduler:
- operates in user space
- uses decentralized, multi threaded appraoch (Goroutines are not all limited to 1 thread)

G - light weight user-space task managed by GO runtime
P - a logical scheduling context owned by the GO runtime => its not a CPU core
M - an OS thread (actual pthread on linux; windows thread on Windows)
* many Gs -> multiplexed on to P, P maintains a run queue of runnable goroutines & minimizes locking by keeping scheduling decisions decentralized (it is literally a context)
* by default # of Ps map to the same # of CPUs BUT, they are not the same thing 
* only Ms holding a P can execute code, at most 1 M run GO code on 1 P at a time (the thread needs a scheduling context to know what to execute)
* GO routines depend on kernel threads + user-space scheduling

Considerations:
- why not just run G on M?
    - since M is real OS thread, it might get blocked on syscalls
    - P can be detached & handed to another M
    - prevents goroutine starvation
- but doesnt user-space scheduling mean that the OS needs to keep context switching to the user space scheduler?
    - no, this context switch happens in user space => NO syscall, NO kernel context switch, NO trap into OS
    - user-space register save
    - stack pointer swap (literally a pop on the stack)
- what if i run a multi core system that tries to execute the go scheduler together? wouldnt there be multiple Ms (since 1 thread can run on 1 core at once, so if i have 4 cores, i can run 4 threads) then there would be 4 go schedulers running? [MISCONCEPTION]
    - there is only 1 one runtime scheduler; there wouldnt be 4 GO schedulers
    - there would just be 4 threads scheduled on the 4 cores, each core now runs the GO Scheduler code + P's scheduling context
    - M that owns a P executes the scheduler logic using that P's state => goroutines can now be executed
    - Each P is not a scheduler as they only manage local run queue, whereas all 4 M + P run in parallel using this scheduler algorithm

In essence:
OS schedules M
M runs Go code
Go code calls Go scheduler (normal function call)
scheduler picks next goroutine execution continues

# -------------------------------------------------------------------------------------------------
## net.Conn & io.ReadCloser interfaces
- net.Conn is an interface
- io.ReadCloser is an interface as well
```go
type Conn interface {
    Read(b []byte) (n int, err error) // this takes in a buffer to read to btw: buf := make([]byte, 4096), n, err := conn.Read(buf)
    Write(b []byte) (n int, err error)
    Close() error
    LocalAddr() Addr
    RemoteAddr() Addr
    SetDeadline(t time.Time) error
    SetReadDeadline(t time.Time) error
    SetWriteDeadline(t time.Time) error
}
type ReadCloser interface {
    Reader
    Closer
}

type Read interface {
    Read(p []byte) (n int, err error)
}

type Closer interface {
    Close() error
}

var rc io.ReadCloser
var c net.Conn
rc = c // OK
c = rc // NO, BAD => rc does not implement all rc's methods
// net.Conn is a superset of io.ReadCloser
```

* Core rule of types & interfaces: if a type implements all methods an interface, it IS that interface
    => net.Conn implements Read & Close
    => THUS net.Conn implements io.ReadCloser interface
* net.Conn is not literally an io.ReadCloser BUT it implements that interface so it can be passed anywhere a io.ReadCloser is required

# -------------------------------------------------------------------------------------------------
## log vs fmt
- fmt => for formatting & user output
    - no timestamps
    - no metadata
    - no concurrency guarantees
    used for users, CLIs/ tools, tests/ debugging, etc.
- log => for diagnostic output
    - timestamped
    - thread-safe
    - centralized output dest.
    - explicitly not user-facing
    used for emit logs for devs, server-side code, debugging production behaviour

* when writing GO server & you require logs to tri-age future issues, use log!!
* for errors, GO does not havea special "error logging" mechanism (unlike python's log levels info, warn, error)
    => the idiomatic way is to use log.Println("") // if required, write custom "[INFO]..." & "[ERROR]..." strings within the log statement
https://chatgpt.com/share/6985ed28-5d94-800a-83ba-97115fddbaa4


# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
## Miscellaneous Notes/ Fun Facts
-  RFC (request for comments) - official technical doc that defines how the network protocol works
    - is a published doc by the IETF (internet engineering task force) => some org that standardises protocols that allow the internet to function LOL

# -------------------------------------------------------------------------------------------------
## boot.dev cli installation
- this course required me to download the boot.dev CLI to run the test cases against my local env (refer to github to install @ https://github.com/bootdotdev/bootdev?tab=readme-ov-file#installation)
[GO-installation]
```bash
joechua@r-98-107-25-172 ~ % curl -sS https://webi.sh/golang | sh


>>> Welcome to Webi! - modern tools, instant installs.  <<<
    We expect your experience to be absolutely perfect!

    Success? Star it!   https://github.com/webinstall/webi-installers
    Problem? Report it: https://github.com/webinstall/webi-installers/issues
                        (your system is Darwin/arm64 with libc & curl)

Bootstrapping Webi
    Downloading https://webi.sh/packages/webi/webi.sh
        to ~/.local/bin/webi
    Running ~/.local/bin/webi golang@stable

Installing go ...
    Found  ~/.local/bin
    Initializing ~/.config/envman/
    Edit ~/.bashrc to source ~/.config/envman/load.sh
    Edit ~/.zshrc to source ~/.config/envman/load.sh
    WARN: possible PATH conflict between 'go1.25.6' and currently installed version
    /Users/joechua/.local/opt/go/bin/go (new)
    /usr/local/go/bin/go (existing)
    Downloading go from
      https://dl.google.com/go/go1.25.6.darwin-arm64.tar.gz
    Saved as ~/Downloads/webi/go/1.25.6/go1.25.6.darwin-arm64.tar.gz
    Extracting ~/Downloads/webi/go/1.25.6/go1.25.6.darwin-arm64.tar.gz
    Installing to ~/.local/opt/go-v1.25.6/bin/go
    Removing /Users/joechua/.local/opt/go-v1.25.6
    Moving go
      to ~/.local/opt/go-v1.25.6
Installed 'go v1.25.6' to ~/.local/opt/go

    Edit ~/.config/envman/PATH.env to add:
        ~/.local/bin
        ~/.local/opt/go/bin
        ~/go/bin

>>> ACTION REQUIRED <<<
        Copy, paste & run the following command:
        source ~/.config/envman/PATH.env
        (newly opened terminal windows will update automatically)

joechua@r-98-107-25-172 ~ % 
```
boot.dev installation
```bash
joechua@r-98-107-25-172 http_protocol % bootdev --version
bootdev version v1.23.3
joechua@r-98-107-25-172 http_protocol %
```
test submission
```bash
Please navigate to:
https://boot.dev/cli/login

Logged in successfully!
joechua@r-98-107-25-172 http_protocol % bootdev run b0cebf37-7151-48db-ad8a-0f9399f94c58
╭───────────────────────────────────────╮
│ Running: echo "bootdev cli is ready!" │
╰┬──────────────────────────────────────╯
 ├─  ?  Expect exit code 0
 ├─  ?  Expect stdout to contain all of:
 │       - 'bootdev cli is ready!'      

 > Command exit code: 0
 > Command stdout:

bootdev cli is ready!
joechua@r-98-107-25-172 http_protocol % bootdev run b0cebf37-7151-48db-ad8a-0f9399f94c58 -s
╭──────────────────────────────────────────╮
│ ✓  Running: echo "bootdev cli is ready!" │
╰┬─────────────────────────────────────────╯
 ├─  ✓  Expect exit code 0
 ├─  ✓  Expect stdout to contain all of:
 │       - 'bootdev cli is ready!'      

 > Command exit code: 0
 > Command stdout:

bootdev cli is ready!


All tests passed! 🎉

Return to your browser to continue with the next lesson.

joechua@r-98-107-25-172 http_protocol % 
```