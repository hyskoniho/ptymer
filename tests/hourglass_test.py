import sys
sys.path.insert(1, r'.\src')

from ptymer import HourGlass
from time import sleep

#####################################################################
#                                                                   #
#                                                                   #              
#                        HOURGLASS TESTS                            #                                      
#                                                                   #
#                                                                   #
#####################################################################

# Simple test
def hourglass_test():
    hg = HourGlass(seconds=5, visibility=True).start()
    sleep(5)

def comparative_tests():
    hg1 = HourGlass(seconds=5, visibility=True).start()
    sleep(0.5)
    hg2 = HourGlass(seconds=5, visibility=True).start()
    sleep(0.5)
    print(f"HourGlass 1 is greater than HourGlass 2: {hg1 > hg2}")
    print(f"HourGlass 2 is greater than HourGlass 1: {hg1 < hg2}")
    print(f"HourGlass 1 is equal HourGlass 2: {hg1 == hg2}")
    print(f"HourGlass 1 is greater or equal than HourGlass 2: {hg1 >= hg2}")
    print(f"HourGlass 2 is greater or equal than HourGlass 1: {hg1 <= hg2}")
    print(f"HourGlass 1 is different than HourGlass 2: {hg1 != hg2}")
    sleep(5)

def func_tests():
    hg = HourGlass(seconds=5, visibility=True).start()
    sleep(2)
    print(f"Current time: {hg.remaining_time()}")
    sleep(2)
    print(f"Current seconds: {hg.remaining_seconds()}")
    sleep(1)
    hg.stop()

# Error tests
def comparative_error():
    hg1 = HourGlass(seconds=5, visibility=True).start()
    sleep(0.5)
    hg2 = 50
    sleep(0.5)
    print(f"HourGlass 1 is greater than HourGlass 2: {hg1 > hg2}")
    print(f"HourGlass 2 is greater than HourGlass 1: {hg1 < hg2}")
    print(f"HourGlass 1 is equal HourGlass 2: {hg1 == hg2}")
    print(f"HourGlass 1 is greater or equal than HourGlass 2: {hg1 >= hg2}")
    print(f"HourGlass 2 is greater or equal than HourGlass 1: {hg1 <= hg2}")
    print(f"HourGlass 1 is different than HourGlass 2: {hg1 != hg2}")
    sleep(5)

if __name__ == "__main__":
    print("\nTeste 1:")
    hourglass_test()
    sleep(1)
    print("\nTeste 2:")
    comparative_tests()
    sleep(1)
    print("\nTeste 3:")
    func_tests()
    sleep(1)
    print("\nTeste 4:")
    comparative_error()