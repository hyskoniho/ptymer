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
    b = HourGlass(seconds=10, visibility=True, persist=True, target=print, args=("Function executed!")).start()
    sleep(11)
    print(b)

if __name__ == "__main__":
    hourglass_test()