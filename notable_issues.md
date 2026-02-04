# notable issues

This file contains notable issues i faced during my development journey. It
helps with easy reference when i faced the same/ similar issue.
Think of it like doing on-call support where you'd refer to past similar issues to
debug your current problems -- it significantly reduces your tri-age time.

---------------------------------------------------------------------------------------------------
## HWE package referencing missing kernel headers
I was trying to install curl on my system (running Ubuntu OS) when i noticed an error
post installation:
`E: Sub-process /usr/bin/dpkg returned an error code (1)`
Curl was definitely installed (validated by running `curl --version`)

### research
- printed out the different kernel versions on my system & the 1 im currently booted into
```bash
joe@joe-VivoBook-ASUSLaptop-X412FJ-X412FJ:~/Desktop/DEV/go_server$ dpkg -l | grep linux-image
ii  linux-image-6.11.0-26-generic                 6.11.0-26.26~24.04.1                     amd64        Signed kernel image generic
ii  linux-image-6.14.0-37-generic                 6.14.0-37.37~24.04.1                     amd64        Signed kernel image generic
ii  linux-image-6.8.0-39-generic                  6.8.0-39.39                              amd64        Signed kernel image generic
ii  linux-image-generic-hwe-24.04                 6.11.0-26.26~24.04.1                     amd64        Generic Linux kernel image
joe@joe-VivoBook-ASUSLaptop-X412FJ-X412FJ:~/Desktop/DEV/notes$ uname -r
6.8.0-39-generic
```
    - linux-image-6.8.0-39-generic => is the 1 im booted into now
    - linux-image-6.11.0-26-generic => is installed for some reason; HWE meta packages point to this version of the kernel
    - linux-image-6.14.0-37-generic => NVIDIA packgs are building against this one; kernel headers missing
    - linux-image-generic-hwe-24.04 => meta package, not a kernel itself
- HWE meta packages points to `linux-image-6.11.0-26-generic` => check via 
- our system has a new kernel version installed as well and NVIDIA kernal packages are kernel-version-specific
    - i.e. `linux-modules-nvidia-535-6.14.0-37-generic`
    - when package unpacks, dpkg must: build/verify kernel modules for 6.14.0-37, using headers for 6.14.0-37
- few things to note:
    0. ubuntu LTS (long term support) releases such as 22.04 or 24.04 provide stability with a 5 year supported kernel
        - HWE(hardware enablement) stack is an optional upgrade for these systems
        - offers newer kernels with drivers for modern HW
        * LTS software refers to SW versions that are supported with updates, bug fixes & security patches for a longer period of time(years) which these versions release requested features that are provided out of cycle
        * the term `HWE` is specific to ubuntu; although, other distros also ship "newer kernel for older releases"
    1. ubuntu OS version is independent of the kernel version
        - ubuntu ver -> userlandm libs, tools ,release cadence
        - kernel version -> HW suppport, drivers, low lever OS core
    2. linux allows multiple kernels to coexist on 1 ubuntu system
    3. kernal headers are C header files (.h), build scripts, linked scripts (i.e. module.lds), makefile fragments
        - describes kernal internals, not user space APIs
        - not used to run the OS
        - used to build kernel modules(i.e. nvidia.ko, wifi drivers, fs drivers etc.) => hence does not stop ubuntu from running
        * user space programs like curl are not kernal modules!! (think back to cs2106 where kernel modules were the specific things like FS drivers)
    4. dpkg vs apt
        - apt is a high lvl, user friendly package manager which uses dpkg as its low lvl backend utility => it auto finds, downloads & installs all required dependencies (using dpkg)
        - dpkg handles the basic installation & removal of indiv .deb files 

### overview & resolution
- currently system has NVIDIA packgs that are half-configured/ installed & bounded to kernel 6.14.0-37
- apt fails becoz it cant finish configuring them withou the kernel headers

1. need to remove current NVIDIA packages
2. install official meta-packages(the missing headers basically) => ubuntu can keep us on the candidate kernel going forward (6.14.0.37)
3. re-install NVIDIA packages against the correct kernel

- useful commands:
```bash
uname -r # unix name command returns info about the system & its HW; -r displays the kernel release number => actual functional version i.e. 5.15.0; -v kernel version focuses on build timestamp & build number from source
dpkg -l | grep linux-image # dpkg is a low-level package mgmt tool used on debian based-linux systems; -l lists all installed packages
apt show linux-generic-hwe-24.04 # shows which kernel the HWE modules depend on => look at Depends: ...; shows 6.14.0-37... is the current candidate
apt-cache policy linux-headers-6.14.0-37-generic # check whether the kernel headers are installed; in this case Installed: (none)
```

what i did:
1. remove nvidia's attachment to stray kernel
2. re-anchor the system to the 
```bash
sudo apt update     # updates APT's local package index => allows apt to know the latest versions avail in ubuntu 24.04 repo
sudo apt upgrade    # upgrades the already installed packgs to the newest ver (since we have the latest list now)
sudo apt install linux-generic-hwe-24.04 linux-headers-generic-hwe-24.04 # installs the HWE meta packages for ubuntu 24.04 => anchors the system to the officially supported HW kernel track (6.14)
sudo apt install linux-headers-6.14.0-37-generic # explicitly installs kernel headers for kernel version 6.14
sudo apt --fix-broken install # attempts to fix broken dependencies & complete the configurations => retry fixing the broken NVIDIA kernel modules now that correct headers are in BUT it might only install headers, & source, download & unpack .deb files, but not finish the configuration
sudo dpkg --configure -a # helps to ensure the configuration is complete
sudo reboot # reboot to boot into the newly installed kernel version
uname -r # validate its the correct version
ls /usr/src | grep $(uname -r) # verify headers exist
sudo ubuntu-drivers autoinstall # install NVIDIA against running kernel, kernel modules exist on disk, BUT may not be loaded into the kernel yet
sudo reboot # kernel modules can sometimes be loaded without reboot, BUT NVIDIA specifically integrates with DRM, display manages hence sages to reboot before validating
nvidia-smi # verify NVIDIA packages are healthy

sudo apt purge 'nvidia-*' 'linux-modules-nvidia-*'
sudo apt install linux-generic-hwe-24.04 linux-headers-generic-hwe-24.04
sudo ubuntu-drivers autoinstall
```

(faced on 04/02/2026; solved on ___)
reference to understand what was going on: https://chatgpt.com/share/69835f44-67b0-800a-9ba7-46767adbf6fa

---------------------------------------------------------------------------------------------------

* dates are in the format: dd/mm/yyyy