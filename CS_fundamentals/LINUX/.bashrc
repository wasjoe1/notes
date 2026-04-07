# Setting global exports
export VCPKG_ROOT='/Users/joechua/Desktop/DEV/vcpkg'
export PATH=$VCPKG_ROOT:$PATH # allows terminal to find vcpkg executable in this path

# Aliases for navigation
alias notebooks='cd /Users/joechua/Desktop/DEV/notebooks/'
alias notes='cd /Users/joechua/Desktop/DEV/notes/'
alias scrapers='cd /Users/joechua/Desktop/DEV/projects/scrapers_project'

# Aliases shortcut
alias mysql=/usr/local/mysql/bin/mysql
alias initpy='python3 -m venv env'
alias act='source env/bin/activate'
alias vact='source .venv/bin/activate'
alias deact='deactivate'
alias dact='dact && act' # deactivate & activate env
alias dvact='dact && vact' # deactivate & activate venv
alias srcbrc='source ~/.bashrc'
alias vimbrc='vim ~/.bashrc'
alias codebrc='code ~/.bashrc'

# Aliases for make file
alias mcd='make clean develop'
alias mcdact='make clean develop && act'
alias mft='make format && make test'

# Aliases for cpp proj init (run from project root)
# alias initcpp='cp -r ~/Desktop/DEV/projects/notes/CS_fundamentals/cpp/init_proj/. .'
initcpp() {
	# placeholder path value
	local target_path=""
	
	# Set according to possible locations
	local possible_locations=(
		"/Users/joechua/Desktop/DEV/notes/CS_fundamentals/cpp/init_proj/" # mac
	)
	for loc in "${possible_locations[@]}"; do
		if [[ -d "$loc" ]]; then
			target_path="$loc"
			break
		fi
	done

	# if no target_path found, try to look through from home direct
	if [[ -z "$target_path" ]]; then
		# the below code
		target_path=$(find ~ -path "*/CS_fundamentals/cpp/init_proj") # should have 1 result

		if [[ -z "$target_path" || $(echo "$target_path" | wc -l) -gt 1 ]]; then
			echo "Error: Expected 1 target_path, but found:"
			echo "$target_path"
			return 1 # to stop the function with error
		fi
	fi
	
	# if still no target_path
	if [[ -z "$target_path" ]]; then
		return 1
	fi
	
	echo $target_path
	cp -r "$target_path"/* . # cp the contents of found path to current directory
}

runcpp() {
	# no specific cpp file, reads CMakeLists.txt
	echo "Setting Preset && building files..."
	cmake --preset vcpkg || return 1
	echo "Set Preset && build files generated"
	
	echo "Compile start..."
	cmake --build build || return 1
	echo "Compile done"

	echo "execute executable..."
	local exe_name=$(grep "CMAKE_PROJECT_NAME:STATIC=" build/CMakeCache.txt | cut -d'=' -f2)
	./build/"$exe_name"
}

debugcpp() {
	echo "Setting Preset && building files..."
	cmake --preset vcpkg -DCMAKE_BUILD_TYPE=Debug || return
	echo "Set Preset && build files generated"
	
	echo "Compile start..."
	cmake --build build || return # return used in function; if normal script, use `exit`
	echo "Compile done"

	echo "execute executable..."
	local exe_name=$(grep "CMAKE_PROJECT_NAME:STATIC=" build/CMakeCache.txt | cut -d'=' -f2)
	./build/"$exe_name"
}

# Aliases for git/ git aliases
# alias ga='git add .' # add logic to allow 0 or more args
alias gs='git status'
alias gd='git diff'
alias gb='git branch'
alias gpull='git pull'
alias gpush='git push'
# alias gpr='git pull --rebase origin master' # old comment assuming all my repos use master
ga() {
	if [ $# -eq 0 ]; then
		git add .
	else
		# more than 1 arg
		git add "$@"
	fi
}
gc() {
	git checkout "$*";
}
gcm() {
	git commit -m "$*";
}
gbc() {
	# assumes only 1 branch matches
	git branch | grep "$*" | xargs git checkout
}
gcb() {
	git checkout -b "$*"
}
# old: gpr() {
	#   git pull --rebase origin "$*" # old command that required me to manually put in branch name
	# }
gpr() { # new command that lets me rebase current branch
  local m_branch
  m_branch=$(git branch --show-current) # returns branch name
  git pull --rebase origin "$m_branch"
}
# bash notes:
	# ; -> acts as newline substitute => allow u to put then on the same line
		# technically u can write code like this:
		# if [ condition ]
		# then
		# 	smt
		# fi
	# $# -> returns number of cli/ positional args => dont include script name

	# $@ vs $* -> spltis args by " "
	# $@ -> splits given string by spaces, place user formatted user accordingly with ""
		# i.e. git add $@ -> ga "part 4.jpg" "test case.jpg" => execs: ga part 4.jpg test case.jpg
		# i.e. git add "$@" -> ga "part 4.jpg" "test case.jpg" => execs: ga "part 4.jpg" "test case.jpg"
	# $* -> splits given string by spaces, place entire string in quotes if ""
		# i.e. git add $* -> ga "part 4.jpg" "test case.jpg" => execs: ga part 4.jpg test case.jpg
		# i.e. git add "$*" -> ga "part 4.jpg" "test case.jpg" => execs: ga "part 4.jpg test case.jpg"


# Checks if its an interactive shell, then print
if [[ $- == *i* ]]; then
	echo "./bashrc was sourced"
fi

# Generated for envman. Do not edit.
[ -s "$HOME/.config/envman/load.sh" ] && source "$HOME/.config/envman/load.sh"

# echo "test change" # this would break my hardlink; yea it did LOL; testing if symlink works now; yes it does :))