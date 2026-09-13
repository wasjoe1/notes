# -------------------------------------------------------------------------------------------------
# docker commands

docker run -it --rm ubuntu:24.04 - runs the ubuntu:24.04 image, `exit` command to exit out of the container
    => --rm - ensures that the container's metadata (like logs, file changes etc.) are deleted
docker ps - prints the existing containers
docker images - lists the images

## detach from docker container
ctrl+p, ctrl+q
## reattach to docker container
docker attach <container_id_or_name>

# -------------------------------------------------------------------------------------------------
# colima commands
`colima status` - check if the VM is still running
`colima stop` - clean shut down of linux VM (images, containers & volumes are preserved on VM's virtual disk)
`colima delete` - removes VM's virtual disk completely (images pulled, named volume, etc. everything deleted)

`colima ssh` - opens a ssh(secure shell) session directly with the background linux VM that colima manages
    => interact with the VM's OS itself instead of using docker commands
    => some commands like dmesg

`colima list` - displays key configs (num cores, mem, etc.) for each VM instance

# -------------------------------------------------------------------------------------------------
# using clangd + docker

clangd is installed on macOS
clangd has its own built-in clang frontend (praser + semantic analyzer)
clangd relies on LLVM compiler => needs an external compiler (clangd or gcc) on ur system to find std lib headers
clangd stops at semantic analysis phase of the compiler frontend
    => checks only syntax, type & variable declarations
    => no actual obj file created
    * ensure to include the config `set(CMAKE_EXPORT_COMPILE_COMMANDS ON)` to produce the `compile_commands.json` file which clangd will use

# Issue: macOS GCC + container's compile_commands.json
- clangd (on host) can still understand most gcc compiler flags
- BUT, clangd will fail to look for system headers (i.e. stdio.h) as it tries to use the path layout from the container's ubuntu system
- compile_commands.json also list paths that only exist inside the container (i.e. /opt/vcpkg etc.)
# Fix
- vscode's dev containers
    => run vscode server, including clangd, inside the container
    => local vscode's window becomes a thin client
    => similar to vscode's remote-ssh => vscode connects over ssh, bootstraps small vscode server process on remote machine (real node.js backend, comms over ssh tunnel)
    => dev containers extension => same thing, but docker daemon's API is used to install & launch the same vscode server binary inside the running container
# Steps to fix
- dev container extension procedure
    1. install dev container extension [ms-vscode-remote.remote-containers]
        * its to install & attach a remote session with a container
    2. with container already running in tmux session, in command palette "Dev Containers: Attach to Running Container..." then select running market-infra-dev container from the list
        * running container needs to exist for the vscode server to be ran inside
    3. vscode will open a new window connected to that container
    4. install clangd extension inside this remote window
        * still need the clangd extension on the vscode server that actually reads the current workspace
    5. clangd can now pick up `compile_commands.json` & resolve container-native paths
# Permanent fix (.devcontainer.json)
1. create `.devcontainer/devcontainer.json`
2. write this inside
```json
{
    "name": "market_infra",
    "build": {
        "dockerfile": "../Dockerfile",
        "context": ".."
    },
    "customizations": {
        "vscode": {
            "extensions": [
                "llvm-vs-code-extensions.vscode-clangd",
                "ms-vscode.cmake-tools",
                "twxs.cmake"
            ],
            "settings": {
                "clangd.path": "/usr/bin/clangd",
                "C_Cpp.intelliSenseEngine": "disabled"
            }
        }
    },
    "workspaceFolder": "/workspace",
    "workspaceMount": "source=${localWorkspaceFolder},target=/workspace,type=bind"
}
```
3. through vscode's devcontainer extension,
    - open the proj folder in vscode
    - command palette, select `dev containers: reopen in container` OR `dev containers: rebuild container`
    - it will read the `.devcontainer.json` file (make sure to include `Dockerfile` inside the json file as well)

_difference between .devcontainer.json vs Docekrfile_
* .devcontainer.json - config file which vscode server will use => tells vscode the configs (things to install, mount which /workspace, etc.) for that container
    * specific to vscode
    => some changes only affect how VScode attaches to it (i.e. workspaceFolder) -> no image content changed -> just `Dev Containers: Reopen in Container` required
    => some changes like `build.docekrfile` require full rebuild `Rebuild Container`
* dockerfile - defines the image; whats inside the container
    * specific to docker images/ containers
    => any changes here always require full rebuild since there will be changes made to the image
    => run `docker build -t market-infra-dev .` again

_difference between clangd & clangd extension(LSP server)_
`apt-get install clangd` - installs the language server (not a full compiler)
install clangd extension - LSP(language server protocol) client; launches clangd process & translates editor actions

# -------------------------------------------------------------------------------------------------
# set up project env in docker

- start running the ubuntu image: `docker run -it --rm ubuntu:24.04`
- update apt & install core dev tools: `apt update && apt install -y build-essential`
    => includes system level tools like c & c++ compilers, std libs `libstdc++-dev`, etc.
- cmake? ubuntu:24.04 already includes cmake(3.28+)
- ninja
- vcpkg
- git, curl, zip, unzip, tar, pkg-config (all required for vcpkg)

## dockerfile vs docker commit (snapshot)
dockerfile encourage; docker commit is discouraged
- docker commit is a blackbox => no record of what u did
- not reproducible elsewhere
- no version control => cant revert back to old version when things break

## running the newly created docker image
`docker run -it --rm -v $(pwd):/workspace market-infra-dev -w /workspace bash`
or just `docker run -it --rm -v $(pwd):/workspace market-infra-dev`

- note: `WORKDIR` in Dockerfile only creates `/workspace` dir in the image + set as default starting dir
- volume flag: `-v $(pwd):/workspace` is what truly binds the host path, to the virutal path (container)
    => if u dont type this, /workspace directory still exists (coz of WORKDIR line in dockerfile), but the dir will be empty
- (optional)workdir: `-w /workspace` => docker runtime command equivalent to `WORKDIR` instruction
    => can be used when its an image u dont control
- (optional)default command: `bash` was set as the default command but for ubuntu:24.04 image, its default command is also bash

# -------------------------------------------------------------------------------------------------
# install & setup docker on mac
article: https://medium.com/@guillem.riera/the-most-performant-docker-setup-on-macos-apple-silicon-m1-m2-m3-for-x64-amd64-compatibility-da5100e2557d
chat with google ai: https://share.google/aimode/73shBPjXLI8Qh7URe

1. intsall docker frontend: `brew install docker docker-compose`
docker - only includes the frontend
docker compose - tool for running multi-container apps => ability to launch multiple services at once
    => typically `brew install docker` does not include docker-compose
    => to check, execute `docker compose version`
* brew will auto update itself here

2. install linux VM spawner + docker backend(colima): `brew install colima`
colima - includes wrapper to create lima VM (linux VM) + docker backend(dockerd + backend engine)

3. test spawn linux VM: Run `colima start --arch aarch64 --vm-type vz --mount-type virtiofs --cpu 4 --memory 8`
this starts a linux VM (via apple's built-in virtualization.framework `vz` backend) &
inside that linux VM, docker daemon(dockerd) starts up

architecture: `--arch aarch64` - [default: aarch64 (arm64)]; no diff
virtualization engine: `--vm-type vz` - builds & runs the VM [default: qemu] => `vz` is faster than `qemu` as `vz` is apple's built-in modern virtualization framework
mount: `--mount-type virtiofs` - how files are shared between containers & disk [default: sshfs] => virtiofs gives faster bind mounts
    sshfs - moves files over secure internal network connection; safe but verbose steps
    virtiofs - direct link between Mac filesystem & VM
    * specific performance can be seen when local web servers load pages instantly instead of lagging
CPU provisioned: `--cpu 4` - [default: 2 cores] provisions 4 cores
MEM provisioned: `--memory 8` - [default: 2GB] provisions 8 Gb

* NOTE: after running this command once, running `colima start` in the future will always use this settings

4. verify frontend to backend: run `docker run --rm hello-world`
to verify docker engine is up (backend host is up)
=> confirms the linux VM is booted
=> docker daemon inside is reachable from mac's docker cli

5. `docker run -it --rm ubuntu:24.04` + `apt update && apt install -y build-essential`
- `install -y build-essential`:
    - `-y` just auto confirms "do u want to continue"
    - `build-essential` consists of:
    gcc (C compiler), g++ (c++ compiler), make (build automation), libc6-dev(glibc's dev files; headers like sched.h), dpkg-dev (tools for bilding .deb packages)
verify by executing `find / -name sched.h` => should see the required headers now

6. stop the linux VM running in the background
`colima status` - check if the VM is still running
`colima stop` - clean shut down of linux VM (images, containers & volumes are preserved on VM's virtual disk)
`colima delete` - removes VM's virtual disk completely (images pulled, named volume, etc. everything deleted)

chat reference: https://claude.ai/share/9f519234-ace1-476c-abe7-d0e7264bb849 (search `setting up`)