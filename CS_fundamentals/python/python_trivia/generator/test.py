#!/usr/bin/env python3

# try writing my own generator
# (1) generator functions
def generator():
    num = 0
    while True:
        yield num
        num +=1
print(generator)
gen = generator()
for i in gen:
    print(i)
val = next(gen)
print(val)
