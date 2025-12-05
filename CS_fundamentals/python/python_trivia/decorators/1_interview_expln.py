# decorator function
    # takes in a function to be called
    # returns a function (enhancing the functionality of the function taken in)

# outside u want to call the decorator fn by tak

# idea is that u want to let people use your decorator function
# without them knowing what u are doing under the hood => just know the rough functionality &
# what THEY should do in their function for it to work
# then they just call their function name, but executes the decorator as a whole

def decorator(func_to_take_in):
    def wrapper(*args, **kwargs):
        print("other do smt") # do smt
        func_to_take_in(*args, **kwargs)
        print("other do smt") # do smt
    return wrapper

def func_to_take_in():
    print("naive code wants to do smt")

func_to_take_in = decorator(func_to_take_in) # this is what @ basically does

# naive coder will call the "func_to_take_in" function
func_to_take_in()