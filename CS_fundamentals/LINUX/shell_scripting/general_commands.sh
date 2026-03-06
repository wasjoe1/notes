#!/bin/bash

# 1. Shebangs
# 2. Shell functions
# 3. $* vs $@

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