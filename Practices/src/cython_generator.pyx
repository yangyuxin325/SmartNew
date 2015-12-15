import random
def generate(num):
    while num:
        yield random.randrange(10)
        num -= 1