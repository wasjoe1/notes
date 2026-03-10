# Command prompt commands
there are actually a few shell programs that the windows terminal(terminal emulator) support:
1. command prompt
2. power shell
3. wsl
* terminal emulators are SW window that runs a shell (i.e. bash, zsh, command prompt(cmd.exe) or power shell)

---------------------------------------------------------------------------------------------------
# Zip a folder

---------------------------------------------------------------------------------------------------
# Zip a folder
(command only avaiable in power shell)
```bash
powershell Compress-Archive -Path myfolder -DestinationPath archive.zip
```

- zips the folder myfolder (& its contents) into archive.zip
- can omit the `powershell` part if your already in powershell