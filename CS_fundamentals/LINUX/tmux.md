# tmux
=> keeps shell session alive

tmux new -s dev     - create new tmux session with `-s` specifying the session name
// run some commands here inside the tmux session
ctrl+B, D      - detach tmux session
tmux attach -t dev  - reattach tmux session; `t` means target

forgot to name? rename current session:
tmux rename-session -t <index> <name>

delete/ exit session:
exit or ctrl+D
delete/ exit from outside:
tmux kill-session -t dev

tmux ls - list all sessions currently running
tmux kill-window -t dev:0   - kill just 1 window inside a session, not the whole thing
tmux kill-server            - kills every tmux session at once

create new window:
ctrl + b, c
jump between windows:
next window: ctrl + b, n
prev window: ctrl + b, p
specific window: ctrl + b, <number>
delete window:
exit every single pane, then exit again
force kill window:
Ctrl+B, then :          # opens tmux's command prompt at the bottom
kill-window -t 2        # kills window index 2
force kill from outside:
tmux kill-window -t dev:2

create new pane (split window into pane)
Ctrl+B, %       - split vertically (creates a left/right split)
Ctrl+B, "       - split horizontally (creates a top/bottom split)

move between panes:
Ctrl+B, ←/→/↑/↓
resize panes:
Ctrl+B, ctrl + ←/→/↑/↓

delete pane:
ctrl+D or exit
force kill: ctrl+B, x

* session - whole persistent container (survives detach & attach)
* window - full screen tab within a session
* pane - split within a single window (can see different panes in the same window simultaneously)

to scroll:
need to enter copy-mode: Ctrl+b [
to quit: q