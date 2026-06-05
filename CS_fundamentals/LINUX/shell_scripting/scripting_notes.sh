#!/bin/bash

# 1. Shebangs
# 2. Shell functions
# 3. $* vs $@, and $#
# 4. binary & ternary operator
# 5. set local variable & inline command substitution
# 6. control statements(if) + discard output + redirect output
  # 6.a) COMMAND (exit status)
  # 6.b) double brackets
  # 6.c) curly brackets
  
  # 6.d) flags
# 7. export

# -------------------------------------------------------------------------------------------------
# Shebangs
# the above is a shebang/ hashbang => tells the OS which interpreter should run the script => via the 1st 2 characters
#   #(sharp) + !(bang) = she-bang => i am for real lol
# #!<path_to_interpreter>

# i.e. run
  # ./script.sh => OS reads first line & see #!/bin/bash, then execs /bin/bash script.sh

# some other interpreters include:
  # `#!/usr/bin/env python3`
  # `#!/bin/zsh`
  # `#!/bin/sh`

# -------------------------------------------------------------------------------------------------
# Shell functions
foo() { # becomes a shell function command i.e. `foo hello` is a runnable command from the terminal
    echo "Inside function, \$0 = $0" # $0 - name of the script OR shell
    echo "Inside function, \$1 = $1" # $1 - 1st arg
}
# `foo hello` => $0 = bash(or if using zsh, it might show zsh) && $1 = hello

gpr() {
  git pull --rebase origin "$*" # $* - all positional args
}
# -------------------------------------------------------------------------------------------------
# $* vs $@, and $#
# $* all args combined into 1 string
# $@ args preserved individually
gcm() {
  git commit -m "$*"
}
# gcm fix bug == git commit -m "fix bug"
# $* = "fix bug"

# vs

gcm() {
  git commit -m "$@"
}
# gcm fix bug == git commit -m "fix" "bug"
# $@ = ("fix", "bug")
# BUT
# if u do this instead: gcm "fix bug"
# $@ = ("fix bug") => works

	# $@ vs $*
		# -> both splits args by " "
	# $@ -> splits given string by spaces, split & place string arguments in "", if "" was used [per arg]
		# i.e. git add $@ -> ga "part 4.jpg" "test case.jpg" => execs: ga part 4.jpg test case.jpg
		# i.e. git add "$@" -> ga "part 4.jpg" "test case.jpg" => execs: ga "part 4.jpg" "test case.jpg"
	# $* -> place entire string in quotes if "" is used [all args]
		# i.e. git add $* -> ga "part 4.jpg" "test case.jpg" => execs: ga part 4.jpg test case.jpg
		# i.e. git add "$*" -> ga "part 4.jpg" "test case.jpg" => execs: ga "part 4.jpg test case.jpg"

	# $# -> returns number of cli/ positional args => dont include script name [number of args]

# -------------------------------------------------------------------------------------------------
# 4. binary & ternary operator

# a. bash's ternary operator:
command1 && do_if_success || do_if_fail

# b. binary operator
do_if_success || do_if_fail

# example
gpr() {
  git pull --rebase origin main || git pull --rebase origin master
}
# * note that if main exist but fails for some reason, the 2nd part will still execute
# * not the best design for this command's intent since merge conflict could potentially make this fail
  # coz in bash:
  # 0 -> success
  # non-zer (which is what merge conflict returns) -> failure

# -------------------------------------------------------------------------------------------------
# 5. set local variable & inline command substitution
gpr() {
  local m_branch
  m_branch=$(git branch --show-current) # returns branch name
  git pull --rebase origin "$m_branch"
}
# $ is required to read the variable
  # i.e.
  # var=hello
  # echo "$var" # => returns hello
# during assignment:
  # var=hello   ✅
  # $var=hello  ❌ invalid
# m_branch=(git branch --show-current)  <= incorrect
  # (...) means array assignment, not command execution
  # bash interprets as an array of elements [git, branch, --show-current]
  # $(...) <= use this for command substitution!

# -------------------------------------------------------------------------------------------------
# 6. control statements(if) + discard output + redirect output
gpr() {
  if git ls-remote --exit-code --heads origin main >/dev/null 2>&1; then
    git pull --rebase origin main
  else
    git pull --rebase origin master
  fi
}

# git ls-remote
  # -> lists reference on a remote repo (all branches on remote)
  # i.e.
  # a1b23c4 refs/heads/main
  # d9f8e7a refs/heads/master
# --heads
  # only filter for heads references (i.e. refs/heads/master or refs/heads/main)
# origin main
  # to check if there is a branch named `main` on the remote called `origin`
# --exit-code
  # IMPT: usually git ls-remote always exits successfully, even if branch dont exist
  # but with `--exit-code`, if branch dont exist, exit code == 2
# >/dev/null
  # discards std output
  # else u might see `a1b23c4 refs/heads/main`
# 2>&1
  # redirects stderr (2) to the same place as stdout (1).
  # 0 - std in, 1 - std out, 2 - stderr
# (refer to image.png for example execution)
  # can see that main failed => it did show exit with code 2
  # while master passed

# control statement (if)
if COMMAND ; then
# or
if COMMAND
then
  # ; helps to end the line => is only needed if everything is on 1 line

# ; -> acts as newline substitute => allow u to put then on the same line
		# technically u can write code like this:
		# if [ condition ]
		# then
		# 	smt
		# fi

# 6.a) COMMAND (returns either 1 or 0)
  # exit status
  # 0 - means success (true)
  # 1 - error encountered (false)

# 6.b) double brackets
# example 1: no bracks
if mkdir "$1"; then
  echo "sucess!"
fi
# example 2: use brackets
if [[ -z "$1" ]]; then
  echo "argument 1 is empty" # -z checks the length of the string => returns 0 if len == 0, else 1
fi

# dont do if [[ mkdir $1 ]]
# * double brackets - used for evaluating expressions (check if expression is true)
  # => commands are not ran in [[ ... ]]
  # => it does "variable expansion" => replaces $1 with actual value
  # => evaluates the expression
  # => does "string creation" if no valid expression => i.e. mkdir $1 is turned into a string (command is not executed)

# 6.c) curly brackets
${...} # inside curly braces, bash modifies how a variable is tested
# :-
${arg:-default} # checks if the argument is empty, & if it is, set to default value
# set as literal string
${1:-new_project} # sets to either arg 1 OR default "new_project" string value
# set as value in argument
new_project="new_project_string"
${1:-$new_project}

# :=
# ${1:=$new_project} # IS NOT ALLOWED => bash prevents positional parameters from being overwritten 
${new_project:=some string value} # sets $new_project to string value "some string value"
echo "$new_project" # "some string value" is returned
# try this on the cli: `: ${new_project:=some string value}`
  # => `:` tells the shell to evaluate the expression, but dont run the result

# 6.d) flags

# 6.d) i) -d
# -d is an operator used within a conditional test (square brackets []) to check if a specific path exists
  # [[]] => preferred dont need to wrap variables in double quotes to prevent error if: 
    # - variable is empty OR contain spaces
    # - can use && & || logic operators directly inside the brackets
    # - pattern matching; supposrts wildcards & regex using =~ operator
  # [] => crashes if name has space

  # -d checks folder name relative to current working directory. unless '/' is first charaacter in path

if [[ -d "$folder_name" ]]; then
		echo "Error: $folder_name already exists! Please choose another project name"
		exit 1
	fi

# -------------------------------------------------------------------------------------------------
# export

# - export is a shell command that makes a variable available to child processes
# - wihout export, the variable exists only in the current shell's (current process) local MEM
# - child processes only get a copy of the env, NOT the shell's local variables