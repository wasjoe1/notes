#!/bin/bash

# 1. Shebangs
# 2. Shell functions
# 3. $* vs $@
# 4. binary & ternary operator
# 5. set local variable & inline command substitution
# 6. control statements(if) + discard output + redirect output

# -------------------------------------------------------------------------------------------------
# Shebangs
# the above is a shebang/ hashbang => tells the OS which interpreter should run the script => via the 1st 2 characters
# # -> sharp + ! -> bang ==> she-bang => i am for real lol
# #!<path_to_interpreter>
# i.e. i run ./script.sh => OS reads first line & see #!/bin/bash, then execs /bin/bash script.sh
# various other interpreters are `#!/usr/bin/env python3`, `#!/bin/zsh`, `#!/bin/sh`

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
# $* vs $@
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