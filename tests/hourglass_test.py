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

if __name__ == "__main__":
    print("\nTeste 1:")
    hourglass_test()
    sleep(1)
    print("\nTeste 2:")
    comparative_tests()