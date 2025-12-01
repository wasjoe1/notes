# notes.md
Contains notes in general when i dont have a sufficient content/ header for an entire file for
Can also be used as a consolidation for shortcut look ups for important notes

# Gitignore-ing specific files & folders
# Terminal & Daemon processes
# True daemon vs Nohup processes
# Setting up jupyter notebook

# -------------------------------------------------------------------------------------------------
# Gitignore-ing specific files & folders
- create a .gitignore file in ur project root
- use these patterns
    - *.log               # Exclude ALL .log files anywhere in the project
    - env/                # Exclude ALL folders named 'env' anywhere
    - something           # Exclude ALL files named 'something' anywhere
    - something/          # Exclude ALL folders named 'something' anywhere
    - something_*         # Match any file starting with 'something_'
    - *something_*        # Match any file containing 'something_' anywhere in name
    - *something_*.txt    # Match files ending with specific pattern (i.e. something_one.txt, something_three.txt)

# -------------------------------------------------------------------------------------------------
# Terminal & Daemon processes
## Daemon
A daemon is a specific type of bg process
- no direct user interaction
- detached from any controlling terminal
* a bg process is a general term; daemon is a long-running, system level process that runs in the bg to provide services or perform tasks until the system shuts down

## Terminal (emulator, tabs/windows, shell)
- Each tab in the terminal emulator isntance(basically the app that appears) is typically a process
    => macos(iTerm2, Terminal.app) & linux (GNOME terminal) uses process-per-tab; fork for each tab
- steps when opening a new tab:
    1. terminal application process forks & spawn a terminal emulator process (per tab)
    2. terminal emulator creates & manages a new pseudo-terminal => master-slave pair of files are created for each terminal process (/dev/pts/_X_ for slave's stdin/stdout/stderr & /dev/ptmx for master)
    3. terminal emulator forks a new process (or thread) to execute your default shell; shell starts as a new process/ thread
    4. shell reads startup files & shows prompts
* terminal app(GUI) :> terminal emulator(tab) -> creates pseudo-terminal(/dev/ptmx[master], /dev/pts/X[slave]) :> shell process (zsh, bash, etc.) :> User programs (vim, ls, etc.)
┌─────────────────────────────────────────────────────────────────┐         ┌─────────────────────────────────────────────────────────────────┐
│                    KERNEL SPACE                                 │         │                 Terminal Application (e.g., iTerm2)            │
│                                                                 │         │                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐         │  ┌─────────────────────────────────────────────────────────┐   │
│  │ PTY Pair 1       │  │ PTY Pair 2       │  │ PTY Pair 3       │         │  │ Main Process (GUI, menus, preferences)                  │   │
│  │ Master Buffer    │  │ Master Buffer    │  │ Master Buffer    │         │  │ PID: 1000                                               │   │
│  │ ───────────────  │  │ ───────────────  │  │ ───────────────  │         │  └─────────────────────────────────────────────────────────┘   │
│  │ Slave Buffer     │  │ Slave Buffer     │  │ Slave Buffer     │         │                              │                                  │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘         │        Creates new tab/window via fork() or spawn             │
│           │                      │                      │                 │                              │                                  │
│    fd 3→┐ │               fd 5→┐ │               fd 7→┐ │                 │  ┌───────────────────────────┴───────────────────────────┐     │
└─────────┼─┼─────────────────────┼─┼─────────────────────┼─┼─────────┘     │  │ Terminal Emulator Process 1 (Tab 1)                   │     │    
          │ │                    │ │                    │ │                 │  │ PID: 1001                                             │     │
    ┌─────┴─┴──────┐      ┌─────┴─┴──────┐      ┌─────┴─┴──────┐            │  │                                                       │     │
    │ Terminal     │      │ Terminal     │      │ Terminal     │            │  │ 1. open("/dev/ptmx") → gets master fd                 │     │
    │ Emulator 1   │      │ Emulator 2   │      │ Emulator 3   │            │  │ 2. Creates /dev/pts/0                                 │     │
    │ (iTerm Tab 1)│      │ (iTerm Tab 2)│      │ (Gnome Term) │            │  │ 3. fork() + exec() → starts bash (PID: 1002)          │     │
    │              │      │              │      │              │            │  │ 4. Manages I/O between terminal UI and /dev/pts/0     │     │
    │ fd 3 →       │      │ fd 5 →       │      │ fd 7 →       │            │  └───────────────────────────────────────────────────────┘     │
    │ /dev/ptmx    │      │ /dev/ptmx    │      │ /dev/ptmx    │            │                              │                                  │
    └──────┬───────┘      └──────┬───────┘      └──────┬───────┘            │                              │                                  │
           │                      │                      │                  │  ┌───────────────────────────┴───────────────────────────┐     │
           ▼                      ▼                      ▼                  │  │ Terminal Emulator Process 2 (Tab 2)                   │     │
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐               │  │ PID: 1003                                             │     │
    │ /dev/pts/0  │      │ /dev/pts/1  │      │ /dev/pts/2  │               │  │                                                       │     │
    │ (Slave 1)   │      │ (Slave 2)   │      │ (Slave 3)   │               │  │ 1. open("/dev/ptmx") → gets DIFFERENT master fd       │     │
    └──────┬──────┘      └──────┬──────┘      └──────┬──────┘               │  │ 2. Creates /dev/pts/1                                 │     │
           │                      │                      │                  │  │ 3. fork() + exec() → starts zsh (PID: 1004)           │     │
    ┌──────┴──────┐      ┌──────┴──────┐      ┌──────┴──────┐               │  │ 4. Manages I/O between terminal UI and /dev/pts/1     │     │
    │ bash        │      │ zsh         │      │ fish        │               │  └───────────────────────────────────────────────────────┘     │
    │ (PID 1001)  │      │ (PID 2001)  │      │ (PID 3001)  │               │                                                                 │
    └─────────────┘      └─────────────┘      └─────────────┘               └─────────────────────────────────────────────────────────────────┘

## tmux (terminal multiplexer)
Terminal App → Terminal Emulator (Tab 1) → tmux client → tmux server (TTY manager; daemon)
                                                              │
                                                              ├── Window 1 (PID 1004): /dev/pts/5 → bash
                                                              ├── Window 2 (PID 1005): /dev/pts/6 → vim
                                                              └── Window 3 (PID 1004): /dev/pts/7 → python
* each tmux session is a separate process,proof:
    i.e. 
    - Window 1:
    $ echo "Window 1: PID=$$, TTY=$(tty)"
    Window 1: PID=1004, TTY=/dev/pts/5
    - Window 2:
    $ echo "Window 2: PID=$$, TTY=$(tty)"
    Window 2: PID=1005, TTY=/dev/pts/6  # DIFFERENT PID, DIFFERENT TTY!
* has only 1 tmux server process (TTY manager) that manages ALL the pseudo terminals
tmux server process(TTY manager) :> MANY pseudo terminals(TTY) :> shell process (1-1 with TTY)
    - tmux server multiplexes many TTYs through 1 connection to the real terminal
* tmux server is a daemon process => is not killed when ur terminal apps closes

# -------------------------------------------------------------------------------------------------
# True daemon vs Nohup processes

# -------------------------------------------------------------------------------------------------
# Setting up jupyter notebook
0. Create & activate env
1. Install the jupyter noteboook pip packages
2. Install the packages u want to use
3. Start a tmux session
4. Start the jupyter kernel & web server
5. Detach the tmux session

0. Create & activate env
```bash
python3 -m venv env # create a virtual env with the folder named 'env'
source env/bin/activate # or use my shortcut act
```

1. Install the jupyter noteboook pip packages
```bash
pip install notebook jupyterlab
```
* notebook vs jupyter vs jupyterlab
- jupyter - gives u the kernel & core(core pckg, client, console etc.) but no web interface;
            vscode uses jupyter kernel (installed via jupyer or ipykernel) to run cells, does not need notebook as vscode provides its own interface
- notebook - gives u the notebook server (web interface; basically host static files) & the kernel(if not already installed)
- jupyterlab - gives u the jupyterlab server(modern web interface) & the kernel

* core refers to the fundamental libraries that provide the basic infra for jupyter i.e. manage configs, run the kernel gateway etc.

2. Install the packages u want to use
```bash
pip install pandas
```

3. Start a tmux session
```bash
tmux # use indexed name
tmux new -s jupyter_server # or use a custom name
```
* tmux server is a daemon process so server will not be killed when the current terminal is terminated

4. Start the jupyter kernel & web server
```bash
jupyter notebook    # classic notebook interface
jupyter lab         # modern interface
```

5. Detach the tmux session

# -------------------------------------------------------------------------------------------------
