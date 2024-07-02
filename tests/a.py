import sys
sys.path.insert(1, r'.\src')

from ptymer import Timer, HourGlass
from time import sleep

# Timer test
def timer_test():
    a = Timer(visibility=True)
    a.mark("First mark")
    sleep(3)
    a.mark("Second mark")
    sleep(2)
    a.stop()

# HourGlass test
def hourglass_test():
    b = HourGlass(visibility=True, persist=True, func=lambda: print("Function executed!")).start()
    sleep(5)
    b.stop()

if __name__ == "__main__":
    with Timer(visibility=True) as t:
        for x in range(10):
            t.mark(f"Mark {x+1}")
            print(x)
            sleep(1.2)