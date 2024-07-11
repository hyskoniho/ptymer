import sys
sys.path.insert(1, r'.\src')

from ptymer import Alarm
from time import sleep

#####################################################################
#                                                                   #
#                                                                   #              
#                          ALARM TESTS                              #                                      
#                                                                   #
#                                                                   #
#####################################################################

# Simple test
def target():
        print("Alarm!")

def alarm_test():    
    alarm = Alarm(target=target, args=(), schedules=["20:50:00"], visibility=True).start()
    sleep(100)

if __name__ == "__main__":
    print("\nTeste 1:")
    alarm_test()