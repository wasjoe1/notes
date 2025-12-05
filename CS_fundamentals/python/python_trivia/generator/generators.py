# generators => special kind of function that return a lazy iterator => do not store their content in mem
# common cases is to work with data streams or large files
def gen_infinite():
    num = 0
    while True:
        yield num
        num+=1
gen = gen_infinite()
print(next(gen))
print(next(gen))

# --------------------------------------------------------
# check if its palindrome
def is_palindrome(num):
# Skip single-digit inputs
    if num // 10 == 0:
        return False
    temp = num
    reversed_num = 0

    while temp != 0:
        reversed_num = (reversed_num * 10) + (temp % 10)
        temp = temp // 10

    if num == reversed_num:
        return True
    else:
        return False

# infinite palindrome generator
def infinite_palindromes():
    num = 0
    while True:
        print("num", num)
        if is_palindrome(num):
            i = (yield num) # yield can be an expression as well; expression returns a value
            print("i", i)
            if i is not None:
                num = i
        num += 1

# main code
pal_gen = infinite_palindromes() # if next is not called, generator function is not executed
print("next cmd:", next(pal_gen)) # next has to be called first to start the generator, this returns the value yielded
print("pal_gen:", pal_gen.send(10)) # this will send back a value to the placed where it yielded & set i to be 10 (if it was another next call, i would be set to None)
                          # and the generator will continue running to return the next yielded value

# send()
# for i in pal_gen:
#     digits = len(str(i))
#     pal_gen.send(10**(digits))
#     print(i)

# throw() & close()
for i in pal_gen:
    print(i)
    digits = len(str(i))
    if digits == 5:
        pal_gen.throw(ValueError("We don't like large palindromes"))
        # pal_gen.close() # can use close instead which will return StopIteration error
    pal_gen.send(10 ** (digits))    

# build pipelines
file_name = "techcrunch.csv"
lines = (line for line in open(file_name)) # generator of lines
list_line = (s.rstrip().split(",") for s in lines) # remove spaces on the right & split by ,
cols = next(list_line) # this will contain the first row, which is usually column names
# i.e. cols = ['name', 'age', 'location'] => when the first line of techcrunch.csv is name,age,location