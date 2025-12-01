i.e. script:
```bash
#!/bin/bash
foo() {
    echo "Inside function, \$0 = $0"
    echo "Inside function, \$1 = $1"
}
```
i.e. command
```bash
foo testArg
```

* $0 is the script's name (if executed as an interactive shell session, its the shell's name i.e. bash OR zsh)
* sha-bang from #! => informs OS which interpreter should be used to run the rest of the script
    * OS looks at first 2 bytes => interprets the rest of the line as path to the interpreter

* shell scripts are not executables
    * files are made executable
    * but its not a binary executable
    * plain text file containing commands written for a shell interpreter
    
* execution steps:
    * current shell calls OS to execute that file
    * OS reads 1st 2 bytes (#!) => notices its a script & starts an interpreter for it
    * it then runs: /bin/bash ./myscript.sh
    * bash program does the actual execution

reference: https://chatgpt.com/c/690ff516-e42c-8320-bf9e-48927191eff5 