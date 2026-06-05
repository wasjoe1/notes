# language specs

- type
- compiled or interpreted
- garbage collection

## type

static + strong

static - type checking happens at compile time
strong - strict type rules, no implicit type conversion


## compiled or interpreted

Java is considered both _compiled_ & _interpreted_

*javac* - compiler
__Src code (.java)__ --compiled by java compiler(javac)--> __java bytecode (.class)__
* java bytecode(.class) is platform-independent, not HW specific machine code

*JVM's interpreter*
__java bytecode(.class)__ --runs by the interpreter in the JVM--> __machine code__
* JVM contains an interpreter that reads bytecode (.class) line-by-line & translater it into native machine code

*JVM's JIT compiler*
* JVM monitors bytecode while it is running & identifies frequently executed hotspots
* JIT compiler compiles these hotspots into native machien code & store them in MEM for future executions


## garbage collection

GC is an automatic MEM meanagement process performed by the JVM - removes unreachable objects from heap MEM

*main idea* - run GC once heap filled
The main idea is that once heap MEM is filled, JVM runs GC to (1) mark ref-ed & un-ref-ed objects, then (2) clear up unreferenced objects
    - step 1: marking - mark ref & un-ref objects
    - step 2: delete - delete un-ref objects
    - step 2a: deletion w compacting - delete un-ref objects & compact ref objects

*generational GC*
JVM further splits heap MEM into generations. minor GC is run once young generation section is filled, major GC is run when old generation is filled. full GC is done for permangent generation
    - minor GC - young generation
    - major GC - old generation
    - full GC - permanent generation

references:
- compiled or interpreted: https://medium.com/@pranjalmehta183/is-java-both-compiled-and-interpreted-080a8dbe8ec5
- GC: https://www.oracle.com/webfolder/technetwork/tutorials/obe/java/gc01/index.html