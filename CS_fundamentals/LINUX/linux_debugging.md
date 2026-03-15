# Kill commands
kill <pid>              # SIGTERM by default [15]
kill -15 <pid>          # graceful termination
kill -9 <pid>           # forceful kill
kill -SIGTERM           # same as 15    => signal is handled by the process; it can be caught or ignored by process
kill -SIGKILL           # same as 9     => kill processi s by the kernel; cant be ignored

# List processes
ps aux | grep <name>
ps -p <pid> -f          # -p: indicate pid; -f: full format => show info about process w pid
<!-- joechua@192 DEV_GRIND % ps -p 370 -f
  UID   PID  PPID   C STIME   TTY           TIME CMD
    0   370     1   0 27Sep25 ??         0:00.32 /usr/sbin/KernelEventAgent -->

# Process resources
pidstat -urd
    # -u => show CPU usage
    # -r => MEM/ RAM
    # -d => file I/O

# Process's socket
lsof -p <pid>           # used to list all file sockets opened by stated process
strace -p <pid>         # is attached to a running process & intercepts & logs the system calls that the process makes

# Socket's process
ss -lntp | grep <port>   # shows the socket that is opened on port + corresponding process
    # -l => listening sockets only
    # -n => dont resolve hostname; show raw ips & ports
    # -t => tcp sockets
    # -p => show process pid & name for each socket

# Process tree
pstree -ps <child_pid>      # shows the ancestors (tree upwards from the child)
    # -p => show for pid
    # -s => show ancestors
pstree -p <pid>

# Networks commands
# Host connectivity
ping <domain/ip_address>        # uses ICMP echo & reply; can check both reachability & delay
    # -c => limits the number of ICMP echo messages made
    <!-- ping google.com -->
    <!-- ing 8.8.8.8 -->
    <!-- ping -c 4 google.com -->
traceroute <domain>             # can use ICMP/ UDP packets, TTL & ICMP type 11 (Time exceeded error) https://www.cloudflare.com/learning/network-layer/what-is-mtr/

# Host & Port connectivity
telnet <domain> <port>          # only supports TCP
netcat -vz <domain> <port>      # support both TCP & UDP
    # both establish TCP connection with the host:port to check if its listening
    # netcat is more versatile
        # can be verbose, scripted; telnet is usually executed on an interactive terminal
        # UDP does not establish connection, it depends on server to reply with ICMP type 3 (dest. unreachable); nc uses this to infer the port is closed
        # if there's a firewall, ICMP might drop this & u might not get a response

# creating new hardlink
for some reason, my hardlink between `~/.bashrc` and `../.bashrc` was unlinked. i read that sometimes IDEs would save the
file as a new file and hence it might be that the file was replaced.

now in creating a new hardlink:
- need to run the ln <target> <new_file>
- <new_file> cant exist, unless u force overwrite it using `-f` flag => i did this
```bash
joechua@Chuas-MacBook-Air-3 notes % ln ~/.bashrc "/Users/joechua/Desktop/DEV/projects/notes/CS_fundamentals/LINUX/.testrc"
ln: /Users/joechua/Desktop/DEV/projects/notes/CS_fundamentals/LINUX/.testrc: File exists
# above failed ^ as i created the file
joechua@Chuas-MacBook-Air-3 notes % ln -f ~/.bashrc "/Users/joechua/Desktop/DEV/projects/notes/CS_fundamentals/LINUX/.testrc"
# force overwrite ^
joechua@Chuas-MacBook-Air-3 notes % 
```
- renaming the file that is hardlinked is possible & still maintains the hardlink (i changed from `.testrc` -> `.bashrc`)

# copy entire folder to path
```bash
cp -r ../folder_name target/path
# i.e. cp -r ../cpp_orderbook "/Users/joechua/Desktop/DEV/projects/notes"
```
- common mistake is doing `cp -r . target/path` which copies the content of the current folder
- ensure that u reference the folder using `../target_folder` instead of `.`, else all contents are poured into the `target/path`
- this happens coz creating a folder named `.` inside another dir doesnt make sense

# copy folder content to path
```bash
alias initcpp='cp -r ~/Desktop/DEV/projects/notes/CS_fundamentals/cpp/init_proj/* .'
```
- `cp -r mydir target`  	creates `target/mydir`
- `cp -r mydir/* target`	copies contents (no hidden files)
- `cp -r mydir/. target`    copies contents (including hidden files) => use this so .gitignore & .clang-format is copied over

# delete files inside current directory
- rm -r *       deletes content only
- rm -rf        what does this exec?
    - rm -rf *      this is actl what is executed; deletes content only
- `rm -rf * .*`       deletes hidden contents too (expants to `*` + `.*` => but not good command tbh since it tries to del `.` & `..`)

# list debugging commands (for files) [ls]
1. check to see if files are hardlinked
- `ls -l` see how many references are there to the current inode
    ```bash
    joechua@Chuas-MacBook-Air-3 notes % ls -l "/Users/joechua/Desktop/DEV/projects/notes/CS_fundamentals/LINUX/.bashrc"
    -rw-r--r--  1 joechua  staff  1624 Mar 13 11:06 /Users/joechua/Desktop/DEV/projects/notes/CS_fundamentals/LINUX/.bashrc
    ```
    * this shows 1 reference only
- `ls -i` see the inode number of a file
    ```bash
    joechua@Chuas-MacBook-Air-3 notes % ls -i "/Users/joechua/Desktop/DEV/projects/notes/CS_fundamentals/LINUX/.bashrc"
    105223875 /Users/joechua/Desktop/DEV/projects/notes/CS_fundamentals/LINUX/.bashrc
    ```
    * this shows the inode number to be `105223875`

2. check to see if file is a symlink
```bash
# ls -l 
joechua@Chuas-MacBook-Air-3 bin % ls -l c++
-rwxr-xr-x  78 root  wheel  118880 Feb 25 11:41 c++
# not symlinked; symlinks have 1st letter `l` instead of a - (e.g., lrwxr-xr-x).
```

3. understanding owner & group with access
```bash
# owner: root, group: wheel
joechua@Chuas-MacBook-Air-3 bin % ls -l c++
-rwxr-xr-x  78 root  wheel  118880 Feb 25 11:41 c++
# owner: root -> system administrator acc
# group: wheel -> special group reserved for system administrators (can use su command to become the root user)

# owner: joechua, group: staff
joechua@Chuas-MacBook-Air-3 puzzle_1 % ls -l puzzle_1.py 
-rw-r--r--  1 joechua  staff  757 Dec 10 01:23 puzzle_1.py
# owner => i created
# user group => general "user" group on my mac can access
    # staff is for User files
    # (reminder that u can check ur group using the `group` command)
```
* __su, sudo, root & wheel, admin__
    - root -> dont need to use sudo coz it has the highest privileges
    - sudo (superuser do) -> is a tool for normal user (like joechua) to temporarily act with root powers
        -> exec 1 command with that root's perms
    - su (switch user) -> to completely log in to the user (usually root), to have access to that user's permissions
    - wheel -> is the `Superuser` group
    - admin -> is the group for human users who can temporarily use sudo to gain root powers

4. finding out if the file is a wrapper/ stub
* its actually pretty hard to know even with commands like `file` or `ls -l`
    - usually if its a script `file` will output `"Bourne-Again shell script", "Perl script text executable", "ASCII text"` etc.
    - then u can check the shebang `head -n 1 /path/to/your/file`
- in general, its good to know that for macOS, in `/usr/bin` almost everything inside it is a system stub
    - running `file` on `/usr/bin/python3` & `/usr/bin/git` will have roughly the same output
    - it does this so when u update ur software (like the compiler), the path to execute the software is still the same
