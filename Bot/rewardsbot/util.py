import random
import time


def wait(delay):
    print('waiting', delay)
    time.sleep(delay)


def wait_random():
    wait(random.uniform(.5, 2))
