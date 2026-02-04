# Aliases for navigation
alias notebooks='cd /Users/joechua/Desktop/DEV/notebooks/'
alias notes='cd /Users/joechua/Desktop/DEV/notes/'
alias scrapers='cd /Users/joechua/Desktop/DEV/projects/scrapers_project'

# Aliases shortcut
alias mysql=/usr/local/mysql/bin/mysql
alias createenv='python3 -m venv env'
alias act='source env/bin/activate'
alias vact='source .venv/bin/activate'
alias deact='deactivate'
alias dact='dact && act' # deactivate & activate env
alias dvact='dact && vact' # deactivate & activate venv
alias srcbrc='source ~/.bashrc'
alias vimbrc='vim ~/.bashrc'

# Aliases for make file
alias mcd='make clean develop'
alias mcdact='make clean develop && act'
alias mft='make format && make test'

# Aliases for git/ git aliases
alias ga='git add .'
alias gs='git status'
alias gd='git diff'
alias gb='git branch'
alias gpull='git pull'
alias gpush='git push'
alias gpr='git pull --rebase origin master'
gc() {
	git checkout "$*";
}
gcm() {
	git commit -m "$*";
}
gbc() {
	git branch | grep "$*" | xargs git checkout
}
gcb() {
	git checkout -b "$*"
}

# Checks if its an interactive shell, then print
if [[ $- == *i* ]]; then
	echo "./bashrc was sourced"
fi

# Generated for envman. Do not edit.
[ -s "$HOME/.config/envman/load.sh" ] && source "$HOME/.config/envman/load.sh"
