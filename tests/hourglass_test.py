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
    
    print(f"hg1 >= hg2: {hg1 >= hg2}")
    print(f"hg1 <= hg2: {hg1 <= hg2}")
    print(f"hg1 == hg2: {hg1 == hg2}")
    print(f"hg1 != hg2: {hg1 != hg2}")
    print(f"hg1 > hg2: {hg1 > hg2}")
    print(f"hg1 < hg2: {hg1 < hg2}")

if __name__ == "__main__":
    print("\nTeste 1:")
    hourglass_test()
    sleep(1)
    print("\nTeste 2:")
    comparative_tests()