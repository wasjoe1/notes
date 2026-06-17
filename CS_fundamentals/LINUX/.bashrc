# Set global exports
# PATH is an env variable that holds a list of dir paths separated by colons
	# export tells shell to make env variable available to any child process
export VCPKG_ROOT=~/Desktop/DEV/vcpkg # home in Dev
export PATH=$VCPKG_ROOT:$PATH # allows terminal to find vcpkg executable in this path
export PATH="$HOME/.local/bin:$PATH" # enables claude bin to be found on ubuntu OS (linux)

# notes
export notes=~/Desktop/DEV/notes

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

# bashrc
alias srcbrc='source ~/.bashrc'
alias vimbrc='vim ~/.bashrc'
alias codebrc='code ~/.bashrc'

# notes
alias codenotes='code /Users/joechua/Desktop/DEV/notes'

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
		"~/Desktop/DEV/notes/CS_fundamentals/cpp/init_proj/" # generic
		"/Users/joechua/Desktop/DEV/notes/CS_fundamentals/cpp/init_proj/" # mac
		"/home/joe/Desktop/DEV/notes/CS_fundamentals/cpp/init_proj/" # ubuntu
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
	
	# VERSION 1: implicit check + copy contents
	# echo $target_path
	# # create a new directory
	# folder_name="new_project"
	# mkdir ${1:-$folder_name} # not using -p because i want it to throw an error & not go silent when such a folder already exists
	# 	# actually -p only makes it such that the line fails, but the script still runs as there is no exit command

	# # copy contents into new directory
	# cp -a "$target_path"/. ./${1:-$folder_name} # cp the contents of found path to current directory
	
	# cp -a "$target_path"/* . # leaves out hidden files
	# cp -a "$target_path" . # copies folder; not folder content
	# cp -a "$target_path"/. . # copies folder content
	# cp .clang-format .gitignore ../cpp_dijkstras
		# cp always treats the last arg as the dest path
		# if there exists these files inside that dir, files will get overwritten => use -v for verbosity
		# cp -n .clang-format .gitignore ../cpp_dijkstras # no clobber => doesnt add files that already exist
	
	# VERSION 2: explicit check + copy dir (not contents)
	# set the folder name
	folder_name="${1:-new_project}"
	# check if the folder exists already => exit if it does
	if [[ -d "$folder_name" ]]; then
		echo "Error: $folder_name already exists! Please choose another project name"
		exit 1
	fi

	# copy dir (instead of content) to curr dir && rename in 1 shot
	cp -a "$target_path" "$folder_name"
}

runcpp() {
	# no specific cpp file, reads CMakeLists.txt
	echo "Setting Preset && building files..."
	cmake --preset vcpkg || return 1
	echo "Set Preset && build files generated"
	
	echo "Compile start..."
	cmake --build build || return 1
	echo "Compile done"

	echo $'Executing executable(auto skip a line):\n'
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

	echo $'Executing executable(auto skip a line):\n'
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

# Checks if its an interactive shell, then print
if [[ $- == *i* ]]; then
	echo "./bashrc was sourced"
fi

# Generated for envman. Do not edit.
[ -s "$HOME/.config/envman/load.sh" ] && source "$HOME/.config/envman/load.sh"

# echo "test change" # this would break my hardlink; yea it did LOL; testing if symlink works now; yes it does :))