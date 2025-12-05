# ----------------------------------------------------------------------------------------------------------------------------------
# Unpacking zip files
import zipfile
import io # io.BytesIO wraps a bytes object in a file-like object => helps u to create in-mem files & dont need to write to disk
from pathlib import Path
from typing import Tuple

ZIP_PATH: Path = "zipfile.zip"

def iter_zip_bytes(data: bytes) -> Iterator:
    with zipfile.ZipFile(io.BytesIO(data), "r") as z:
        for name in z.namelist():
            with z.open(name) as f:
                data = f.read()
                if name.endswith(".zip"):
                    yield from iter_zip_bytes(data)
                else:
                    yield name, data

def iter_zip_files(file_path: Path) -> Iterator[Tuple[str, bytes]]:
    with open(ZIP_PATH, "rb") as f:
        content = f.read()
    yield from iter_zip_bytes(content)
# OR
def iter_zip_files(file_path: Path) -> Iterator[Tuple[str, bytes]]:
    # open a zip file
    # iterate through all the files inside
    # read them 1 by 1 => yielding each content
    with zipfile.ZipFile(file_path, "r") as z:
        # for all the file names in z
        for name in z.namelist():
            # open the file in z
            with z.open(name) as f:
                data = f.read() # zip or file data
                if name.endswith(".zip"):
                    yield from iter_zip_bytes(data) # yield from means u want to yield every file inside a generator (if u only yield, u are just returning the generator as a value)
                else:
                    yield name, data

# methd 1
content = None
with open(ZIP_PATH, "rb") as f:
    content = f.read()
for file_name, file_data in iter_zip_bytes(content):
    print(file_name, file_data)
# methd 2
for file_name, file_data in iter_zip_files(ZIP_PATH):
    print(file_name, file_data)
    pass

# ----------------------------------------------------------------------------------------------------------------------------------
# generating numbers
from typing import Iterator

def generate_numbers() -> Iterator:
    for i in range(1001):
        yield i # pauses & returns the value

gen = generate_numbers() # returns a generator object

print(next(gen))  # 0
print(next(gen))  # 1
print(next(gen))  # 2

for num in generate_numbers():
    # for loop gets an iterator from this:
    # i.e. iterator = iter(gen)
    # and then repeatedly calls num = next(iterator)
    print(num)

# This is actually what the "for loop" does under the hood
gen = generate_numbers()
while True:
    try:
        num = next(gen)
    except StopIteration: # stop iteration exception is raised when you run out of items in your generator
        break
    # body of the for loop

# ----------------------------------------------------------------------------------------------------------------------------------
# EXPLANATION
# Iterable	An object you can loop over	__iter__()
# Iterator	The actual object that produces items one at a time __iter__() + __next__()
# nums = [1, 2, 3] => iterable; iterable is not necessarily an iterator
# it = iter(nums) => iterator; the object that remembers & produces the next item when asked
    # get an iterator from any iterable: iterator = iter(iterable)
# generator function => special iterator-like object that remember its state & resumes from last yield

# Summary:
# *Iterable → must define __iter__
# *Iterator → must define __iter__ and __next__
# *Generator → is a special subclass of Iterator that Python creates when it sees a yield

from collections.abc import Iterable, Iterator, Generator

def generate_numbers():
    yield from range(3)

lst = [1, 2, 3]
it = iter(lst)
gen = generate_numbers()

print(isinstance(lst, Iterable))   # True
print(isinstance(lst, Iterator))   # False
print(isinstance(lst, Generator))  # False

print(isinstance(it, Iterable))    # True
print(isinstance(it, Iterator))    # True
print(isinstance(it, Generator))   # False

print(isinstance(gen, Iterable))   # True
print(isinstance(gen, Iterator))   # True
print(isinstance(gen, Generator))  # True
