import sys
sys.path.insert(1, r'.\src')

from ptymer import Timer, HourGlass
from time import sleep

# Timer test
@Timer(visibility=True)
def timer_test():
    for x in range(10):
        print(x)
        sleep(0.8)

# HourGlass test
def hourglass_test():
    b = HourGlass(visibility=True, persist=True, func=lambda: print("Function executed!")).start()
    sleep(5)
    b.stop()

if __name__ == "__main__":
    timer_test()