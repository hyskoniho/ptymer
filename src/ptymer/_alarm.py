from datetime import datetime
from typing import Callable, Any, List, Tuple, Union, Optional
from dataclasses import dataclass
from dateutil import parser
from psutil import Process as psProcess, pid_exists
from time import sleep
from multiprocessing import Process, freeze_support

@dataclass
class Alarm():
    schedules: List[Union[datetime, str, Tuple[int, int, int, int, int, int]]]
    # list of datetime objects
    target: Callable
    # function that will be executed when the alarm is triggered
    args: Tuple[Any] = ()
    # arguments of the function
    visibility: bool = False
    # defines if the alarm will show messages or not
    persist: bool = False
    # if true, the alarm will not be elimnated after being triggered
    __pid: Optional[int] = None
    # process id of the alarm

    def __post_init__(self) -> None:
        """
        Post initialization method, checks if the schedules and other
        attr are valid and converts strings to datetime objectsr
        """
        if not isinstance(self.schedules, list):
            raise TypeError("Schedules must be a list!")
        elif not self.schedules:
            raise ValueError("Schedules must be defined!")
        elif not self.target:
            raise ValueError("Target function must be defined!")
        elif not isinstance(self.target, Callable):
            raise TypeError("Target must be a function!")
        elif not isinstance(self.args, tuple):
            raise TypeError("Arguments must be a tuple!")
        elif not isinstance(self.visibility, bool):
            raise TypeError("Visibility must be a boolean!")
        elif not isinstance(self.persist, bool):
            raise TypeError("Persist must be a boolean!")
        else:
            for idx, date_obj in enumerate(self.schedules):
                try:
                    assert (type(date_obj) in [datetime, tuple, str])
                    if type(date_obj) == str:
                        self.schedules[idx] = parser.parse(date_obj)
                    elif type(date_obj) == tuple:
                        self.schedules[idx] = datetime(*date_obj)
                        # converting tuple(d, h, m, s) to datetime object
                    elif type(date_obj) == datetime:
                        self.schedules[idx] = date_obj.replace(microsecond=0)
                        # truncating microseconds
                except:
                    raise TypeError(f"Invalid datetime object: {date_obj}")
                finally:
                    pass

    def __str__(self) -> str:
        return f"Class Alarm()\nVisibility: {self.visibility}\nSchedules:\n {[str(schedule) for schedule in self.schedules]}\nTarget function: {self.target}\nArguments:\n {[arg +': ' + str(type(arg)) for arg in self.args]}\nPersist: {self.persist}\nProcess id: {self.__pid if self.__pid and pid_exists(self.__pid) else None}\n"
    
    def start(self) -> "Alarm":
        """
        Setup alarm
        """
        from os import getpid
        freeze_support()
        
        if self.__pid and pid_exists(self.__pid):
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
        while len(self.schedules) > 0 and pid_exists(mainPid):
            now = datetime.now().replace(microsecond=0)
            try:
                idx = self.schedules.index(now)
            except:
                sleep(0.1)
                continue
            else:
                print("Alarm finished!") if self.visibility else None

                self.run_function(self.target, *self.args)
                self.schedules.pop(idx) if not self.persist else None
            
        self.__pid = None
    
    def stop(self) -> None:
        """
        Stop the alarm
        """
        if self.__pid and pid_exists(self.__pid):
            process = psProcess(self.__pid)
            process.terminate()
            self.__pid = None
        else:
            raise RuntimeError("Alarm not set!")
        
        print("Alarm stopped!") if self.visibility else None

if __name__ == "__main__":
    pass