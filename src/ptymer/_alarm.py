from datetime import datetime
from typing import Callable, Any
from dataclasses import dataclass
from dateutil import parser
from psutil import Process as psProcess
from time import sleep

@dataclass
class Alarm():
    """
    Alarm class
    """
    schedules: list[datetime | str]
    target: Callable
    args: tuple[Any] = ()
    visibility: bool = False
    persist: bool = False
    __pid: int | None = None

    def __post_init__(self) -> None:
        """
        Post initialization method
        """
        for idx, date_obj in enumerate(self.schedules):
            try:
                assert (type(date_obj) == datetime or type(date_obj) == str)
                if type(date_obj) == str:
                    self.schedules[idx] = parser.parse(date_obj)
            except:
                raise TypeError(f"Invalid datetime object: {date_obj}")
            finally:
                pass
    
    def start(self) -> "Alarm":
        """
        Setup alarm
        """
        from multiprocessing import Process, freeze_support
        from os import getpid
        freeze_support()
        print("Setting up alarm!") if self.visibility else None
        
        if not self.target:
            raise ValueError("Target function must be defined!")
        elif not self.args:
            raise ValueError("Arguments must be defined!")
        elif not self.schedules:
            raise ValueError("Schedules must be defined!")
        elif self.__pid:
            raise ValueError("Alarm already set!")
        else:
            process = Process(target=self._alarm_loop, args=(getpid(),))
            process.start()
            self.__pid = process.pid
            return self

    @staticmethod
    def run_function(func, *args) -> any:
        """
        Run a function with arguments
        """
        try:
            value = func(*args)
        except:
            pass
        else:
            return value
        
    def _alarm_loop(self, mainPid) -> None:
        """
        Alarm loop
        """
        from psutil import pid_exists

        while len(self.schedules) > 0 and pid_exists(mainPid):
            now = datetime.now().replace(microsecond=0)
            try:
                idx = self.schedules.index(now)
            except:
                sleep(0.1)
                continue
            else:
                self.run_function(self.target, *self.args)
                self.schedules.pop(idx) if not self.persist else None
            
        self.__pid = None
        print("Alarm finished!") if self.visibility else None
    
    def stop(self) -> None:
        """
        Stop the alarm
        """
        from psutil import pid_exists
        if self.__pid and pid_exists(self.__pid):
            process = psProcess(self.__pid)
            process.terminate()
            self.__pid = None
        else:
            raise RuntimeError("Alarm not set!")
        
        print("Alarm stopped!") if self.visibility else None

if __name__ == "__main__":
    a = Alarm(schedules=["2024-07-05 11:11:30"], target=print, args=("Hello", "World"), visibility=True).start()
    print(a)
    print(a.schedules)
    from time import sleep
    sleep(50)
    