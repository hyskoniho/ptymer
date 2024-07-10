import sys
sys.path.insert(1, r'.\src')

from ptymer import Timer
from time import sleep

#####################################################################
#                                                                   #
#                                                                   #              
#                          TIMER  TESTS                             #                                      
#                                                                   #
#                                                                   #
#####################################################################

# Simple test
def timer_test():
    tm = Timer(visibility=True).start()
    sleep(5)
    tm.stop()

# Test with context manager statement
def context_manager_test():
    with Timer(visibility=True) as tm:
        sleep(5)

# Test with decorator statement
@Timer(visibility=True)
def decorator_test():
    sleep(5)

def mark_test():
    tm = Timer(visibility=True).start()
    for x in range(5):
        sleep(0.5)
        tm.mark(f"Mark {x+1}")
        sleep(0.5)
    tm.stop()

def comparative_tests():
    tm1 = Timer().start()
    sleep(0.1)
    tm2 = Timer().start()
    sleep(0.1)
    print(f"Timer 1 is greater than Timer 2: {tm1 > tm2}")
    print(f"Timer 2 is greater than Timer 1: {tm1 < tm2}")
    print(f"Timer 1 is equal Timer 2: {tm1 == tm2}")
    print(f"Timer 1 is greater or equal than Timer 2: {tm1 >= tm2}")
    print(f"Timer 2 is greater or equal than Timer 1: {tm1 <= tm2}")
    print(f"Timer 1 is different than Timer 2: {tm1 != tm2}")
    tm1.stop()
    tm2.stop()

if __name__ == "__main__":
    print("\nTeste 1:")
    timer_test()
    print("\nTeste 2:")
    context_manager_test()
    print("\nTeste 3:")
    decorator_test()
    print("\nTeste 4:")
    mark_test()
    print("\nTeste 5:")
    comparative_tests()