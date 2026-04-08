# just random messy notes

# types of compilers & why its needed
# clang-format

# -------------------------------------------------------------------------------------------------
# types of compilers & why its needed
3 types of C++ compilers
1. gcc      => linux dev
2. clang++  => macOS/ IOS dev
3. msvc     => window dev

actl does it matter what compiler i use? isnt it just compile with any compiler for the rgith system architecture? (i.e. x86. ARM etc.)
- each compiler optimizes for their platform (OS)
- gcc & clang are both open source & cross platform
    - alot of devs install both compilers & stress test on both compilers
    - eventual production grade uses the compiler for that specific platform (OS)
    - each compiler produces the most optimized performance for each of their own platforms (OS)
* most linux distributions (ubuntu, CentOS, Debian) are built using GCC
* MSVC is optimized for windows

for cross-compiling:
- gcc => install specific gcc compiler for that device (i.e. arm-linux-genueabihf-gcc)
- clang => single clang installation targets many architectures, add target flag `--target=arch64-linux-gnu`
- msvc => includes option to cross compile from x64 to ARM64 for windows-on-ARM devices

* architecure - is how the OS talks to the HW; specific assembly instructions + how many bytes for each type + bytes per page + bytes/ word etc.
* OS platform - is how the OS works; diff OS implementations; different syscalls + different implementations of syscalls etc.
* (OS e.g.
As a C++ programmer, you write `std::fstream file("data.txt");`.
Windows compiler: replaces it with code that calls `CreateFileW`.
Linux compiler: replaces it with code that calls `sys_open`.)

# -------------------------------------------------------------------------------------------------
# clang-format
clang-format => formats c & cpp in a certain style (dev was using this to style it according to the style he liked)

* the most popular formatter 

# TODO file
- mark included a TODO, DOING, DONE portion => honestly crazy how i have something like this for my daily taskings while i was in sqpt
- adds it into his .gitignore in the project

- his git commit comment:

main: Fix build errors resulting from clang-format
\n
sub: The code prviously did not declare includes for nay type sused by files. This only worked becuase in almost all
C files, types.h was included as the first include. we've reformatted & changed the ordering which broker that
\n
fix: Fix it now with proper include hygiene.

# -------------------------------------------------------------------------------------------------
# forward declarations

used when theres a file that u need to reference the type but only by a pointer & not the actual type itself.
if you need to reference the actual type, then u have to include the header file

* this makes sense to me coz => all pointers are technically the same size, but if u need the actual obj,
then the compiler must actl know the full size of the type (to know how much MEM to allocate)

```cpp
struct stat;
struct rtcdate;
...
...

int fstat(int fd, struct stat*)
```

# -------------------------------------------------------------------------------------------------
# colour theme update

- wondered why my vscode colour scheme was off
- check colour scheme => goto command paletter (ctrl + shift + p) > perferences: color theme > (was under) `dark 2026` > (changed back to) `dark modern`
- use the following stuff below to test the colours

`test` <== this should be orange/ brown
__test__ <== this should be blue
# test <== this should be blue, both `#` & `test`
```cpp
// comment      <== this should be green
struct stat; // <== struct should be blue, & stat should be green
int fstat(int fd, struct stat*) // <== fstat should be yellow, all others should be some notable colours
```


# -------------------------------------------------------------------------------------------------
# running cpp (own shortcut)

1. `cmake --preset vcpkg` works
2. `cmake --build build` works

* to run in debug mode => for breakpoints

## 1. run in debug mode
- include the -DCMAKE_BUILD_TYPE=Debug flag
    - during `cmake --preset vcpkg -DCMAKE_BUILD_TYPE=Debug`
    - CMake reads `CMakeLists.txt`
    - sees your `CMakeLists.txt`
    - sees `add_executable(app_name main.cpp engine.cpp ...)`
    - then generates makefile/ ninja file where compilation commands include `-g` i.e. `clang++ -g -c main.cpp`

## 2. -c flag
- `-c` means to compile only; doesnt produce an executable => returns an object file (main.o)
- linking phase then you'd stitch .o files tgt into 1 executable
- if no `-c` => linker error
- old way:
    `clang++ -g -c main.cpp -o main.o`
    `clang++ -g -c engine.cpp -o engine.o`
    `clang++ main.o engine.o -o my_trading_app` (The Linking Step)

## 3. debug version (unoptimized)
- debug version usually doesnt reorder code for optimization => might be slower => but importantly its to debug state of your app
- then cmake --build build runs normally => but builds a debug version of it

## Dump
below was just a draft version for the above notes written when i was coming up with `debugcpp`

```bash
debugcpp() {
	# include the -DCMAKE_BUILD_TYPE=Debug flag
		# during cmake --preset vcpkg -DCMAKE_BUILD_TYPE=Debug
		# CMake reads CMakeLists.txt
		# sees your CMakeLists.txt
		# sees add_executable(app_name main.cpp engine.cpp ...)
		# then generates makefile/ ninja file where compilation commands include -g i.e. clang++ -g -c main.cpp
			# -c means to compile only; doesnt produce an executable => returns an object file (main.o)
			# linking phase then you'd stitch .o files tgt into 1 executable
			# if no -c => linker error
			# old way:
			# clang++ -g -c main.cpp -o main.o
			# clang++ -g -c engine.cpp -o engine.o
			# clang++ main.o engine.o -o my_trading_app (The Linking Step)

		# debug version usually doesnt reorder code for optimization => might be slower => but importantly its to debug state of your app
		# then cmake --build build runs normally => but builds a debug version of it

	# check if `cmake --preset vcpkg` works
	# then if `cmake --build build` works
}
```

# -------------------------------------------------------------------------------------------------
# bash scripting notes
```bash
some_func() {
	# 1. separate declaration?
	# local current_directory => no need separate declaration
	# local found_path

	local found_path=$(find ~/ -path "*/CS_fundamentals/cpp/init_proj") # should have 1 result
	# 2. set current directory => just use .
	# current_directory=$(pwd)
	
	# 3. cp instruction
	# 1st attempt: cp -r $found_path/* $current_directory # cp the contents of found path to current directory
		# a. " " <= around $found_path was added to make sure even path names with spaces can be found
		# b. . <= can just use current directory
		
	cp -r "$found_path"/* . # cp the contents of found path to current directory
}
```

## find command
- `find start_dir`						=> just lists all dirs & sub dirs starting from `start_dir`
- `find start_dir -path "*/some/path"`	=> finds directories with this specific path, need to add *

i.e.
`find ~ -path Desktop` 		=> finds paths that is exactly Desktop; should return nothing
`find ~ -path "*/Desktop"`	=> finds paths that contain Desktop
`find ~ Desktop`			=> retuns all paths inside ~ & Desktop


- Q. how to return only the 1st matching path
	- handle 0 paths
	- handle >1 paths

```bash
some_fn() {
	local paths = $(find ~ -path _some_path_)
	
	# check 0 length
	if [[ -z "$paths" ]]; then echo "Error: cant find directory" # -z checks for empty string ""
	# -z "$string" => checks if the given string has length 0; older shells require "" else it might throw err
	# https://stackoverflow.com/questions/18096670/what-does-z-mean-in-bash

	# check multiple paths


}
```

## conditional command / compound command/ double brackets
- single brackets [] was actl an alias for the test command => [ $a == $b ], varaibles passed as args & executed
- double brackets [[]] is a shell keyword, part of bash language's internal syntax => works on specific shells (bash, ksh, zsh)
- conditional command - it is a builtin language structure designed to __eval expressions__ & return an __exit staus__ => 0 true, 1 false/ error

Q. why [[ ]] over []?
- support for regex
- support for AND OR: && / ` vs -a -o
i.e.
```bash
if [[ $my_var =~ ^[0-9]{4}$ ]]; then
	echo "It's a 4 digit number!"
fi
```

## regex
- `=~` => regex match operator
	- check if string on the left matches pattern on the right
	i.e. `[[ $input =~ ^[0-9]+$ ]]`
- regex
	`^` - means start of string
	`$` - means end of string
	`+` - must have at least 1 or more
	`*` - allows for any occurence, include 0
	i.e. `[[ $input =~ ^[0-9]+$ ]]`
	means, string must start with a digit, contain only digits, then immediately end

## other bash commands
`|` pipe => sends output text of current command, to the next command
`wc -l` word count -lines => counts how many lines of text there are
`-gt n` checks if output number is greater than n
```bash
paths = $(find ~ -path _some_path_)
if [[ ($paths | wc -l) -gt 1]]
```

## common gotachas
- tried to run command on the terminal directly, but couldnt proceed. command executed `if [[ 5 -gt 1]]`
		joechua@Chuas-MacBook-Air-3 ~ % if [[ 5 -gt 1]]
		if cond> echo "greater"
		if cond> fi
		if cond>
		... => it didnt end
	- have to include the space at the end, else the shell cant see the end of the condtion
		joechua@Chuas-MacBook-Air-3 ~ % if [[ 5 -gt 1 ]]
		if> then				<= rmb the `then`!!
		then> echo "hi"
		then> fi
		hi

```bash
# Bad Old Version
paths = $(find ~ -path _some_path_)
if [[ ($paths | wc -l) -gt 1]]
```
- space around bash assignment `some_var = some_val`
	i.e. `paths = $(find ~ -path _some_path_)`
	- bash will think paths is a command& executes using = and the other as args
- using command substitution to get result of a command + echo output of it
	i.e. `if [[ ($paths | wc -l) -gt 1]]`
	- add `$`, `$($paths | wc -l) -gt 1` to execute commands within the () brackets
	- add `echo`, `$(echo $paths | wc -l) -gt 1` to ensure output is generated & piped to wc
		- if you realise, when calling `$paths` on the terminal, it doesnt output anything
		- only when calling `echo` then strings are outputted
		- hence this `echo` is required to pipe output, to the input of the next command
	- add `"..."`, `echo "$paths"` to ensure multiple lines are recorded
		- in bash, if you `echo $var` without `"..."`, the var is turned into 1 long line of text 
		- wc -l will then only see 1 line => erorr check will never trigger
- when error encountered, remember to `return 1`

## scopes
- normal scope
	`my_var="test"`
	- if used in terminal shell, it cant be seen by another shell session => because its another process

- local scope
	`local my_var="test"`
	- meant to be used in a function; when fn ends, its deleted
	- outside a fn, some shells (zsh, mac) will treat as normal variable, BUT other shells (bash) will throw an error
	- if used in terminal shell, it cant be seen by another shell session => because its another process
- global scope
	- works like "Parent-to-Child" tree, not shared among all processes & scripts
	- if used in terminal shell, it cant be seen by another shell session => because its another process
	
* if you want persistent variable, should declare inside .bashrc or .zshrc

## interpret `\n` as newLine + line feeds
depends on how string is declared && how string is echo-ed

```bash
literal_n="test\ntest\ntest\ntest\n" # standard way
ansi_c_n=$'test\ntest\ntest\ntest\n' # ansi-c way using $'...'

echo "$literal_n" # prints 1 line
echo "$ansi_c_n" # prints multiple lines
echo -e "$literal_n" # prints multiple lines # echo -e flag; enable flag; tells echo to interpret backslash escapes
```
* find doesnt return a string with `\n`. it returns raw data that contains actual line feeds
* line feeds - single byte, value 10 in ASCII, is a non-printable invisible character; its just we use \n as the way to mark line break

## finding executable file && executing it

- method 1: => not good
	- 
	```bash
	local exe=$(find build -maxdepth 1 -type f -executable | head -n 1) # find the only executable in the build folder
	"$exe"
	```
	- find starting from `build`, with maxdepth == 1, of file type && executable bit
	- `| head -n 1` -> head commands looks a start of a piece of text, `-n` usually means to hide stuff but in this context its to limit to first n lines from "start"; defaults to 10 lines without -n
* not good => because there might be multiple executables produced

- method 2: => better
	- 
	```bash
	local exe_name=$(grep "CMAKE_PROJECT_NAME:STATIC=" build/CMakeCache.txt | cut -d'=' -f2)
	./build/"$exe_name"
	```
- cut - extract sections from each line of text
- -d - sets delimiter to "="
- -f2 - selects field (column) number 2 => can select any field number starting from 1?

## head & tail

return first n lines; end after nth line
- `| head -5` == `| head -n 5` - return only the top 5 lines
- `| head -n -5` - (inverse) return everything but the last 5 lines => shortcut doesnt work for negative numbers (must use -n flag)

	|
	|
	- <== end

return last n lines; return last lines till nth line
- `tail -n 2` - give last 2 lines
- `tail -n +2` - start at line 2 & give everything until the end

	- <== end
	|
	|

## execute bash file
you have `script.sh`

- method 1: grant perms + run with file path
	chmod +x script.sh
	./script.sh
	* why do i need `./` why not just call `script.sh` to run script?
	- unlike windows, unix based systems DONT look at current folder for programs to run unless u specifically tell them to
		=> only look at folders listed in `$PATH`
		=> AND it only looks at the "first level"/ immediate contents, not subsub directories
		=> pretty print `$PATH` using `tr` translate command to swap out colon(:) separators => `echo $PATH | tr ':' '\n'`

- method 2: bash command
	bash script.sh
	- dont need to change perms

## check if a path (file/ directory) exists
- -d - true if path is a existing dir
- -f - true if path is a existing regular file (not folder)
- -e - true if path exists (file or folder)
- -s - true if file exists & is not empty (size > 0)

```bash
if [[ -d "$path" ]]; then
	# something
fi
```
## MAGIC $PATH on mac

!!WARNING Never ever set a variable to path => Zsh "magic trap"
on MacOS(Zsh), lowercase variable `path` points to uppercase `$PATH`
by setting a variable `local path="..."` now u cant call any builtin functions i.e. `cp` or `ls` etc.
from that script because `$PATH` was overwritten

* learnt this the hard way...

## sync-ing .bashrc across devices
Initally i uused hardlinks to sync my .bashrc across multiple devices

This is a poor method as:
1. only the master device actually gets updated
2. upon making changes on the non-master device, the master device pulls changes & hardlink break (why?)
	- performing `git pull` or `git checkout` when there are changes to a file, creates a temp file with the new content & then moves/ renames it to replace the old one
	- since the file is moved/ renamed, link cease to exists, and .bashrc is never updated (stays the old verseion without changes)

new method 1: (symlink)
- del the current .bashrc => use the `.bashrc` in the git repo as the src of truth
- create a symlink at `~/.bashrc` that points to `.bashrc` in the git repo (i.e. ln -s /git/repo/.bashrc ~/.bashrc => this symlinks ~/.bashrc to the tracked file in ur git repo)

* this was why whenver i made changes to my `.bashrc` using my linux device & pushed changes & pulled it on my mac, my hard link breaks & `~/.bashrc` stops syncing with git repo's `.bashrc`

# -------------------------------------------------------------------------------------------------
## while writing cpp_timer

- use curly braces
	- for type safety
	- prevent "most vexing parse" => to prevent compiler from accidentally declaring a function
	- 
	```cpp
	std::list<int> myList;
	std::vector<int> myVector(std::list<int>(myList).begin(), std::list<int>myList.end()); // u think u are creating vector, but compiler thinks u are declaring function 
	// std::vector<int> myVector(myList.begin(), myList.end()); // this is actl safe because compiler sees that myList.begin() is a member/ variable call (accessing a member/ variable for values)
	```
