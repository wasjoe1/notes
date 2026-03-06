# Linux

## Description
This folder contains my personal notes for anything related to linux debugging

* `../.bashrc` & `~/.bashrc` are hard links to the same inode; This is actually the .bashrc file on my main device (macbook)
=> to check `ls -li ~/.bashrc` & `ls -li ../.bashrc`
=> `-l` is long listing format, `-i` is show inode number
=> notice that they have the same inode number
