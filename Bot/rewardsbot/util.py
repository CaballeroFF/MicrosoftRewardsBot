import random
import time
import string


def random_letter():
    return random.choice(string.ascii_letters)


def wait(delay):
    print('waiting', delay)
    time.sleep(delay)


def wait_random():
    wait(random.uniform(.7, 2))
