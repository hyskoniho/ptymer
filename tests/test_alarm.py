try:
    from ptymer import Alarm
except ImportError:
    import sys
    sys.path.insert(1, r'.\src')
    from ptymer import Alarm
finally:
    from datetime import datetime, timedelta
    import pytest
    from psutil import pid_exists

#####################################################################
#                                                                   #
#                                                                   #              
#                          ALARM TESTS                              #                                      
#                                                                   #
#                                                                   #
#####################################################################

def test_alarm_init():
    a = Alarm([datetime.now() + timedelta(seconds=5)])
    assert len(a.schedules) == 1

    with pytest.raises(TypeError):
        a = Alarm("5")

def test_alarm_start_stop():
    a = Alarm([datetime.now()])
    a.start()
    assert a.status == True
    a.stop()
    assert a.status == False

def test_alarm_wait():
    a = Alarm([datetime.now()+timedelta(seconds=2)])
    a.start()
    a.wait()
    assert a.status == False

def test_alarm_status():
    a = Alarm([datetime.now() + timedelta(seconds=2)])
    assert a.status == False
    a.start()
    assert a.status == True
    a.stop()
    assert a.status == False

def test_alarm_pid():
    a = Alarm([datetime.now() + timedelta(seconds=2)])
    a.start()
    assert a.pid is not None
    assert pid_exists(a.pid)
    a.stop()

    with pytest.raises(AttributeError):
        assert a.pid is None

def test_error_alarm_already_running():
    a = Alarm([datetime.now() + timedelta(seconds=2)])
    a.start()
    with pytest.raises(RuntimeError):
        a.start()

def test_error_alarm_already_stopped():
    a = Alarm([datetime.now() + timedelta(seconds=2)])
    a.start()
    a.stop()
    with pytest.raises(RuntimeError):
        a.stop()

def test_error_alarm_not_started():
    a = Alarm([datetime.now() + timedelta(seconds=2)])
    with pytest.raises(RuntimeError):
        a.stop()