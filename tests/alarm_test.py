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
    alarm = Alarm(target=target, args=(), schedules=["13:54:00"], visibility=True).start()
    alarm.stop()

def attr_acss():
     alarm = Alarm(schedules=["10:49:00"], visibility=True).start()
     alarm.schedules = ["10:50:00"]
     print(alarm.schedules)

def alarm_wait():
    alarm = Alarm(schedules=["15:00:00"], visibility=True).start()
    alarm.wait()

if __name__ == "__main__":
    print("\nTeste 1:")
    alarm_test()
    sleep(1)
    print("\nTeste 2:")
    attr_acss()
    sleep(1)
    print("\nTeste 3:")
    alarm_wait()