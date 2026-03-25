# Storage drives
This document aims to clarify the difference between HDD(Hard disk drive) vs SSD(solid state drives) vs Flash drives

## HDD vs SSD
## SDD vs Flash
## Flashing vs Installation

# -------------------------------------------------------------------------------------------------
## HDD vs SSD
both are data storage devices
- HDD - store data in magnetic disks (older)
- SSD - store data in flash MEM (silicon's physical & chemical properties) for faster, larger & more efficient storage (newer)

reference: (https://aws.amazon.com/compare/the-difference-between-ssd-hard-drive/)

# -------------------------------------------------------------------------------------------------
## SDD vs Flash
- flash is the technology that supports storage on the SDD device
    - flash is a silicon chip-based storage medium that is writeable & erasable via electricity
    - fast, no moving parts, non-volatile MEM, & rewriteable
- SSD is the storage device, defined as 1 that isnt in motion (contrary to a moving arm in HDD)
    - some has the same form factor as HDD => allows us to use solid state storage over disk-based ones
    - most SSDs use flash as their storage medium (not all though); comparison is like CD vs CD drive:
        - CD drive: SSD     => the reader/ writer
        - CD: Flash         => storage medium
reference: (https://www.enterprisestorageforum.com/hardware/flash-vs-ssd-storage-is-there-a-difference/)

# -------------------------------------------------------------------------------------------------
## Flashing vs Installation (flash storage vs drive storage)
__Flash compiled code__
In embedded systems, the phrase "Flash compiled code onto the hardware" is commonly used.
This basically means to write the firmware (a software made for hardware that is rarely changed) to the flash storage.
This flash storage typically refers to the non-volatile storage on the chip itself, and not the external drive storage.

Formal definitions:
- "Flashing" - to write low-level SW called firmware directly onto small dedicated flash MEM chip on the motherboard
- "Installing" - process of copying SW onto a mass storage device like a HDD/ SSD

* installation is not the same as flash-ing compiled code (binary)
* an example is that you'd flash the BIOs/ UEFI on the flash storage of a computer,
but install the OS on to the HDD/ SSD => so the storage which the binary is inserted into are different