# Boot up
This page explains how an OS is installed in ur system &
then how system boot process starts running this OS process (What happens when we turn on computer?).

## How an OS is installed
## How a system is booted

# -------------------------------------------------------------------------------------------------
## How an OS is installed
1. Compile OS code
2. Install OS binary + bootloader (i.e. GRUB) into device

# -------------------------------------------------------------------------------------------------
## How a system is booted

1. system turns on and runs the __BIOs__ (Flash chip)
    i. wakes up the HW
    ii. looks for disk/ storage device
    iii. loads __MBR__ from disk into RAM

2. MBR then finds the bootloader (i.e. __GRUB__ or __windows boot manager__) using the __partition table__
    i. BIOs version [old way]: __MBR__ finds "__Active" partition__ in partition table, then jump to the start of that partition to find the __bootloader__
    ii. __UEFI firmware + GPT (GUID Partition table)__ [new way]: UEFI on chip is smarter => can actually read file systems (i.e. FAT32).
        it looks at partition table to find the __EFI system partition (ESP)__ & looks for specific file `.efi` bootloader inside a folder in that partition
    => old way uses MBR from the HDD/ SSD to find bootloader
    => new way uses firmware from flash chip to find bootloader (dont have to load MBR first)
    => faster coz u can immediately see the files & folders using UEFI; older BIOs was just blind LOL

3. __Bootloader__ (i.e. GRUB) is loaded, and then finds the __OS kernel__ to be load
    specific e.g. for linux + windows dual boot set up on my windows PC:
    i. installed GRUB (SSD partition) which is "polite", thus adding windows entry to its own menu
    ii. during system startup, it is the first bootloader loaded, asking whether linux or windows?
    iii. if linux chosen, loads the linux kernel. if windows chosen, it loads windows bootloader instead
    
    reference: (https://askubuntu.com/questions/347203/what-exactly-is-grub)

4. Finally __OS kernel__ is loaded


* BIOs/ UEFI lives in flash MEM (on the chip)
* MBR(Master boot record) is the program in the 1st 512 bytes on disk
* bootloader lives on storage device (SSD/ HDD); not in BIOs flash MEM
* OS lives in HDD/ SDD
* Dual booting - having 2 OS on 1 device; typically dont share the same bootloader

reference: (https://www.geeksforgeeks.org/operating-systems/what-happens-when-we-turn-on-computer/)