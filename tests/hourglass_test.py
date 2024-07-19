try:
    from ptymer import HourGlass
except ImportError:
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
    hg = HourGlass(seconds=5.3354935, visibility=True).start()
    sleep(5)
    print(hg)

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
    hg = HourGlass(seconds=325.2, visibility=True).start()
    sleep(2)
    print(f"Remaining time: {hg.remaining_time()}")
    print(f"Remaining seconds: {hg.remaining_seconds()}")
    hg.stop()
    sleep(1)    

# Target tests
def target():
    print("1!")
def target2(num):
    print(f"{num}!")

def target_test():
    hg = HourGlass(seconds=2, visibility=True, target=target).start()
    sleep(2.1)
def target_test2():
    hg = HourGlass(seconds=2, visibility=True, target=target2, args=(2,)).start()
    sleep(2.1)

# Error tests
def target_error():
    hg = HourGlass(seconds=2, visibility=True, args=(1,)).start()

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
    try:
        print("\nTest 1:")
        hourglass_test()
        sleep(1)
        print("\nTest 2:")
        comparative_tests()
        sleep(1)
        print("\nTest 3:")
        func_tests()
        sleep(1)
        print("\nTarget Tests:")
        print("\n1:")
        target_test()
        sleep(1)
        print("\n2:")
        target_test2()
        sleep(1)
        print("\nError tests:")
        print("\n1:")
        target_error()
        sleep(1)
        print("\n2:")
        comparative_error()
    except Exception as e:
        print(f"Error: {e}")
        sleep(5)