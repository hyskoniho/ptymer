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
    
if __name__ == "__main__":
    print("\nTeste 1:")
    hourglass_test()