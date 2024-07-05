import sys
sys.path.insert(1, r'.\src')

from ptymer import Timer, HourGlass, Alarm
from time import sleep
from datetime import datetime

# Timer test
@Timer(visibility=True)
def timer_test():
    for x in range(10):
        print(x)
        sleep(0.8)

# HourGlass test
def hourglass_test():
    b = HourGlass(seconds=6, visibility=True, persist=True, target=print, args=("Function executed!",)).start()
    print(f"\n{b}\n")
    sleep(8)
    print(f"\n{b}\n")

if __name__ == "__main__":
    a = Alarm(target=print, args=("CHEGA",), schedules=[datetime.now()], visibility=True).start()
    print(a)
    sleep(10)
    a.stop()