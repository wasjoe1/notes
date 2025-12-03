# general OS commands
last reboot | head          # shows u the last times the OS rebooted
uname                       # returns the name of the operating system; any other OS kernel related info
hostname                    # returns the hostname of the terminal      # i.e. hostname => 192.168.1.16
# process commands
# (process listing)
ps aux | grep <PID>
# (kill process)
kill -9
# (process resource)
# sockets (ports, sockets, file descriptors)
lsof -p <pid>
pidstat

# grep commands
grep <word> <file>              # i.e. grep tmux /var/log/syslog; greps the word "tmux" from ur system's logs
<command> | grep <word>         # i.e. ls | grep hello; grabs hello from the ls output

# mv
shopt -s extglob            # -s: set => turn option on for; extglob => wildcard patterns
mkdir new_folder
mv !(A0258217B.zip|assignment_1|assignment_2) new_folder/

# create symlink/hardlink
ln <target_file> <new_link_name>   # create hardlink (i.e. ln original.txt hardlink.txt)
ln -s <target_file> <new_link_name>   # create symlink (i.e. ln -s original.txt hardlink.txt)
* terminology: <target_file> is actually the original file with content; <new_link_name> is the file that contains the "duplicate"
* creation with relative path: ln original.txt path1/path2/somewhere.txt
* creation with abs path: ln /home/user/original.txt /tmp/backup/somewhere.txt

# create hardlink
# acl permissions
setfacl -m 
setfacl -x
getfacl <dir>

getfacl .                   # returns acl perms for the curr dir

# tmux commands
tmux ls                         # lists sessions
tmux new                        # creates session with session 0
tmux new -s <session_name>      # starts a new sesion with a specified session name i.e. tmux new -s buildP4
tmux attach -t <session_name>   # attaches back a tmux session that u created b4
grep tmux /var/log/syslog       # greps the word "tmux" from ur system's logs
tmux kill-session -t <session_name>     # kills specified tmux sessions via session name
tmux kill-server                        # kills all tmux sessions
ctrl + b (relase) + d => detaches your tmux while leaving it running in th bg
tmux attach -t 0
* normal terminal session:
    - exists only inside your current terminal window/ tab => closing the window means session dies
    - long running processes will be stopped
* advantages of tmux:
    - runs separate from the terminal; can run in the BG
    - virtual env running its own shell; indpt of wtv window youre in
    - can connect to it from any terminal window
    - tmux session still runs even after closing real terminal
* tmux session names use indexes by default unless stated
    i.e.
    (env) joechua@Chuas-Air-3 notebooks % tmux ls
    0: 1 windows (created Mon Dec  1 08:32:34 2025)
    1: 1 windows (created Mon Dec  1 08:32:52 2025)
    2: 1 windows (created Tue Dec  2 00:18:14 2025)
    new: 1 windows (created Tue Dec  2 00:20:19 2025)

# screen
screen -S buildP4       # create & enter a new screen session
ctrl + a, d             # detaches from the screen session
screen -r buildP4       # go back to the screen session
screen -ls              # list all screen sessions
screen -S buildP4 -X quit # kill a screen session (from the outside)

# unzipping a file/ unzip a file
unzip <file>.zip                        # unzips content into <file>; og file is kept
unzip <file>.zip -d <folder_dir>        # unzips content into a specified folder
unzip -l <file>.zip                     # list contents without extracting
# gzip
gzip -d <file>.gz                   # decompress/ uncompress a .gz file
gunzip <file>.gz                    # decompress/ uncompress a .gz file; BOTH CMDS replaces file.gz w 
gunzip -c <file>.gz > file          # keep the og .z file & -c writes output to stdout

# copy content
cat file.txt > file.out             # writes the contents of file.txt into file.out (file.out content overwritten)
cat file.txt >> file.out            # appends contents of file,txt into file.out (file.out content not overwritten)
<file_read_from> < <file.in> > file.out    # file_read_from reads from file.in & this output is then written out to file.out
                                            # i.e. envsubst < file.in > file.out
envsubst    # small cli-utility that replaces env vars placeholders in text with their curr values
            # it reads text from stdin & writes out to std out

# finding shell
echo $0             # returns bash or zsh
echo $SHELL         # returns /bin/zsh or /bin/bash

* $0 returns the name of the running process's script OR the shell if its interactive
* $1, $2 ... returns the positional parameters then
i.e.
#!/bin/bash
echo "This script is called: $0"
<!-- returns: This script is called: ./myscript.sh --> can see that $0 == script name

# preview/ show lines in a file (first & last)
head <file>             # shows the first few lines of a file (default: 10)
head -n 5 <file> | nl   # shows first 5 lines inside the file with line # prepended
head -n 5 <file>        # shows first 5 lines inside the file
tail -n 5 <file>        # shows last 5 lines inside the file

# nl(number lines) command
takes a file as input & prepends a line number to each line inside the file

# git commands
git diff HEAD^ HEAD             => to see the diff between previous commit to current HEAD commit
git diff HEAD^ HEAD --name-only => shows just the files that have changed
git diff HEAD^ HEAD -- <filepath> =. shows the difference
git stash                       => stashes ur current changes
git stash list                  => lists all the stashed changes
git stash clear                 => clears all stashed changes
git stash show stash@{0}        => shows the difference between the stashed changes & the commit where you made the stash, not the current state of my working direcotry
git stash pop
git stash pop stash@{n}         => pops the specifc changewhere n is the specifc index Zto pop
git stash apply stash@{n}         => applys the specifc change where n is the specifc index to apply, without popping the change
git stash drop stash@{0}        => deletes a specific stashed change
git branch -d branch_name       # Only deletes if branch is merged
git branch -D branch_name       # force deletes a local branch even if its not merged yet
git remote -v # shows u list of remote repos (can fetch, pull, push from these URLs)
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git # change the remote URL associated with origin
git branch -r                   # lists all the remote branches
git remote rm <remote_name>
git fetch origin                # fetch all the latest updates/ branches
git checkout "feature/branch"   # checkout the feature branch from origin
git pull --rebase orign master  # rebases the current branch on the master
- rename branch name
git branch -m <new-branch-name>                     # if ur on the branch u want to rename
git branch -m <feature-oldname> <feature-newname>   # if ur not on the branch u want to rename
- whenever there is a change in ../_ci or ../_template:
`git submodule update --init --recursive`
# remove untracked files
git clean -nd           # show previes of what would be removed
git clean -fd           # actually remove the things that are previewed

# number of lines from a command's output/ file
some_command | wc -l            => returns # of lines
echo "hello world" | wc         => returns 3 columns (# of lines, # of words, # of bytes)
wc file.txt                     => returns 3 columns (# of lines, # of words, # of bytes)

# see permissions
ls -l # return the permissions for each file from the perspective of the current user

# list directories
ls -l | grep '^d'

# file permissions
test -w ./ && echo "writable" || echo "not writable"
test -r ./ && echo "writable" || echo "not writable"

# get/ set acl permission for users
getfacl <dir> # i.e. getfacl /sqpc/hpc/scratch/bd_data_dev/

setfacl -m u:user:x <dir>
setfacl -m u:user:rwx <dir>
setfacl -m u:user:r-X <dir>
setfacl -R -m u:user:r-X <dir> # recursively set the perms for all directories
setfacl -R -m u:user1:r-X,u:user2:r-X <dir>  # sets perms for multiple users
setfacl -d -m u:user:rwx <dir>     # sets default perms for any newly created file/directory
setfacl -d -m o:rx <dir>          # sets default perms (rx) for others
setfacl -x u:user <dir>
* -m means to modify
* -x means to delete the entry (could be a user)

i.e.
setfacl -m u:bd_risk_comp:x /sqpc/hpc/scratch/bd_data_dev/
setfacl -d -m u:alice:rwx mydir     # Alice gets default rwx on 'mydir'
setfacl -d -m o:rx /share
setfacl -m u:bd_vmmprod:rwx .       # modify perms for user
setfacl -x u:sp_dse_prod .          # delete perms

x   -> means you can cd into the directory but cant list; but once u can cd into a directory and that directory has r-X perms for "Others", u have perms to ls in that dir
    -> if u try to list, there is an error
r   -> read perms means u can ls

*references
    https://man7.org/linux/man-pages/man1/setfacl.1.html
    https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/storage_administration_guide/acls-setting-default

# shell commands
- declaring local variable in shell
variable=$(_value_)
    * this is plain assignment; makes variable_name available only in the current shell (not to subprocesses)
    i.e.
        foo=bar
        echo $foo    # shows bar
        bash -c 'echo $foo'   # shows nothing
- delcare as an environment variable; available to child processes (commands/ scripts u run later on)
export foo=bar
bash -c 'echo $foo'   # shows bar
- $ vs ${}
echo "$HOME_dir"        # tries to use $HOME_dir, which might not be set!
echo "${HOME}_dir"      # expands $HOME, then adds _dir
- command substitution $(command)
places returned value from the command into the variable or execution
* variable usage: files=$(ls /tmp)     # 'files' contains the list of files in /tmp
* command usage: echo "My home is at $(pwd)"