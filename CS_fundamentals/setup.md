# SETUP
Some setups to do to make the coding of cpp smoother

# clang format

# -------------------------------------------------------------------------------------------------
# clang format
ensures that ; and indentations are auto done for u
1. download `C/C++` extension
2. download `clangd` extension
3. in the root folder of the project, create .clang-format file & paste this:
```
BasedOnStyle: LLVM
IndentWidth: 4
AccessModifierOffset: -4
```
4. have these settings in vscode IDE:
```
    "editor.autoClosingBrackets": "always",
    "editor.defaultFormatter": "ms-vscode.cpptools",
    "editor.formatOnType": true,
    "editor.autoIndent": "full",
    "C_Cpp.clang_format_fallbackStyle": "LLVM",
    "C_Cpp.intelliSenseEngine": "disabled",
```
