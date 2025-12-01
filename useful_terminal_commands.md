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
