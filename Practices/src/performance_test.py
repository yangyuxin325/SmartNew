import timeit
import random

def generate(num):
    while num:
        yield random.randrange(10)
        num -= 1
        
def create_list(num):
    numbers = []
    while num:
        numbers.append(random.randrange(10))
        num -= 1
    return numbers

print(timeit.timeit('sum(generate(999))', setup="from __main__ import generate", number=1000))
print(timeit.timeit('sum(create_list(999))', setup="from __main__ import create_list", number=1000))

from ctypes import cdll
def generate_c(num):
    libc = cdll.LoadLibrary("libc.so.6")
    while num:
        yield libc.rand() % 10
        num -= 1
        
print(timeit.timeit('sum(generate_c(999))', setup="from __main__ import generate_c", number=1000))

