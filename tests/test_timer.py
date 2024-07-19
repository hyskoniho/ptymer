try:
    from ptymer import Timer
except ImportError:
    import sys
    sys.path.insert(1, r'.\src')
    from ptymer import Timer
finally:
    from datetime import timedelta
    from time import sleep
    import pytest

#####################################################################
#                                                                   #
#                                                                   #              
#                          TIMER  TESTS                             #                                      
#                                                                   #
#                                                                   #
#####################################################################

def test_timer_init():
    timer = Timer()
    assert isinstance(timer, Timer)

def test_timer_start_stop():
    timer = Timer()
    timer.start()
    assert timer.status == True
    timer.stop()
    assert timer.status == False

def test_timer_restart():
    timer = Timer()
    timer.start()
    timer.restart()
    assert timer.status == True

def test_timer_mark():
    timer = Timer()
    timer.start()
    timer.mark("Test mark")
    assert len(timer.marks) == 1

def test_timer_current_time():
    timer = Timer()
    timer.start()
    assert isinstance(timer.current_time(), timedelta)

def test_timer_context_manager():
    with Timer() as t:
        assert t.status == True
    assert t.status == False

def test_timer_decorator():
    @Timer()
    def test_func():
        return "Test function"

    assert test_func() == "Test function"

def test_timer_eq():
    h1 = Timer().start()
    h2 = Timer().start()
    assert h1 == h2

def test_timer_ne():
    h1 = Timer().start()
    sleep(1)
    h2 = Timer().start()
    assert h1 != h2

def test_timer_lt():
    h1 = Timer().start()
    sleep(1)
    h2 = Timer().start()
    assert h1 < h2

def test_timer_le():
    h1 = Timer().start()
    sleep(1)
    h2 = Timer().start()
    assert h1 <= h2

def test_timer_gt():
    h2 = Timer().start()
    sleep(1)
    h1 = Timer().start()
    assert h1 > h2

def test_timer_ge():
    h2 = Timer().start()
    sleep(1)
    h1 = Timer().start()
    assert h1 >= h2

def test_error_if_timer_already_executing():
    timer = Timer().start()
    with pytest.raises(RuntimeError):
        timer.start()

def test_error_if_timer_already_stopped():
    timer = Timer().start()
    timer.stop()
    with pytest.raises(RuntimeError):
        timer.stop()

def test_error_if_timer_not_started():
    timer = Timer()
    with pytest.raises(RuntimeError):
        timer.stop()