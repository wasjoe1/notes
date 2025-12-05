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
    