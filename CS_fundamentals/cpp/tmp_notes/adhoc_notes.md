# Ad_hoc concepts learnt

This is a list of concepts i looked into while programming/ watching cpp vids/ reading cpp articles

- nested functions - dont exist in cpp
    - have to use lambda functions

- member initializer list (initialize vs construct)
    - initialization

- `static` keyword (external vs internal linkage)
    - static can exist in global scope .cpp files, class & function
    - if in .cpp file, its local to the translation unit (internal linkage)
    - else class & function are external linkage

- linker
    - requires entry point to link obj files into executable
    - takes compiled object files & piece them tgt, finds symbol `declarations` & match with `definitions`
