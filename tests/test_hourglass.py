try:
    from ptymer import HourGlass
except ImportError:
    import sys
    sys.path.insert(1, r'.\src')
    from ptymer import HourGlass
finally:
    from time import sleep
    from psutil import pid_exists
    import pytest

#####################################################################
#                                                                   #
#                                                                   #              
#                        HOURGLASS TESTS                            #                                      
#                                                                   #
#                                                                   #
#####################################################################

def test_hourglass_init():
    h = HourGlass(5)
    assert isinstance(h, HourGlass)

def test_hourglass_start_stop():
    h = HourGlass(5)
    h.start()
    assert h.status == True
    h.stop()
    assert h.status == False

def test_hourglass_multiprocessing():
    h = HourGlass(5)
    h.start()
    assert pid_exists(h.pid)
    h.stop()

def test_hourglass_remaining_time():
    h = HourGlass(5)
    h.start()
    sleep(2)
    h.stop()
    assert h.remaining_seconds == 3

def test_hourglass_call():
    h = HourGlass(2)
    h.start()
    h(3)
    assert h.remaining_seconds == 3

def test_hourglass_wait():
    h = HourGlass(2)
    h.start()
    h.wait()
    assert h.status == False

def test_hourglass_eq():
    h1 = HourGlass(5)
    h2 = HourGlass(5)
    assert h1 == h2

def test_hourglass_ne():
    h1 = HourGlass(5)
    h2 = HourGlass(6)
    assert h1 != h2

def test_hourglass_lt():
    h1 = HourGlass(5)
    h2 = HourGlass(6)
    assert h1 < h2

def test_hourglass_le():
    h1 = HourGlass(5)
    h2 = HourGlass(6)
    assert h1 <= h2

def test_hourglass_gt():
    h1 = HourGlass(6)
    h2 = HourGlass(5)
    assert h1 > h2

def test_hourglass_ge():
    h1 = HourGlass(6)
    h2 = HourGlass(5)
    assert h1 >= h2

def target():
        pass
args = ('arg1', 'arg2',)
def test_hourglass_parameters():
    h = HourGlass(seconds=5, target=target, args=args, visibility=True)
    assert h.target == target
    assert h.args == args
    assert h.visibility == True

    h = HourGlass(seconds=5.5, visibility=False)
    assert h.remaining_seconds == 5.5
    assert h.visibility == False

    with pytest.raises(TypeError):
        a = HourGlass(seconds="5", visibility='Yes')

def test_error_if_hourglass_already_executing():
    h = HourGlass(5).start()
    with pytest.raises(RuntimeError):
        h.start()

def test_error_if_hourglass_already_stopped():  
    h = HourGlass(5).start()
    h.stop()
    with pytest.raises(RuntimeError):
        h.stop()

def test_error_if_hourglass_not_started():
    h = HourGlass(5)
    with pytest.raises(RuntimeError):
        h.stop()