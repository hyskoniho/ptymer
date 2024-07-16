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
    target: Optional[Callable] = None
    # function that will be executed when the alarm is triggered
    args: Optional[Tuple[Any]] = None
    # arguments of the function
    visibility: bool = False
    # defines if the alarm will show messages or not
    persist: bool = False
    # if true, the alarm will not be elimnated after being triggered
    __pid: Optional[int] = None
    # process id of the alarm

    def __post_init__(self) -> None:
        """
        Post-initialization method.

        This method validates the attributes and converts string representations of dates 
        to `datetime` objects. It ensures that the schedules, target function, arguments, 
        and other attributes are correctly defined and of the proper types.

        Raises:
            TypeError: If `schedules` is not a list, if `target` is not a callable function, 
                    if `args` is not a tuple, if `visibility` is not a boolean, if `persist` 
                    is not a boolean, or if any schedule entry is not a valid date.
            ValueError: If `schedules` is empty, if `target` is not defined, or if `args` 
                        are defined without a target function.

        Notes:
            - `schedules` should be a list of dates in `datetime`, `tuple`, or `str` format.
            - `target` should be a callable function.
            - `args` should be a tuple of arguments for the target function.
            - `visibility` and `persist` should be boolean values.
            - The method converts string dates to `datetime` objects and tuple dates to 
            `datetime` objects, truncating microseconds for `datetime` objects.
        """
        if not isinstance(self.schedules, list):
            raise TypeError("Schedules must be a list!")
        elif not self.schedules:
            raise ValueError("Schedules must be defined!")
        elif not self.target:
            raise ValueError("Target function must be defined!")
        elif self.target and not isinstance(self.target, Callable):
            raise TypeError("Target must be a function!")
        elif self.args and not isinstance(self.args, tuple):
            raise TypeError("Arguments must be a tuple!")
        elif self.args and not self.target:
            raise ValueError(f"Arguments cannot be defined without a target function!")
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
        Set up the alarm.

        This method initializes and starts the alarm process. It checks if an alarm is already set and 
        raises an error if so. Otherwise, it starts a new alarm process that runs in the background.

        Returns:
            Alarm: The current instance of the `Alarm` class.

        Raises:
            ValueError: If an alarm is already set.

        Notes:
            - This method uses `freeze_support()` to ensure compatibility with Windows.
            - The alarm process is started as a daemon process.
        """
        from os import getpid

        freeze_support()
        # Freeze support for windows

        if self.__pid and pid_exists(self.__pid):
            raise ValueError("Alarm already set!")
        else:
            process = Process(target=self._alarm_loop, args=(getpid(),), daemon=True)
            process.start()
            self.__pid = process.pid
            return self
        
    def run_function(self) -> any:
        """
        Execute the stored function with its arguments.

        This method attempts to run the function stored in `self.__func` with the arguments stored in `self.__args`.
        If no arguments are provided, the function is called without arguments.

        Returns:
            any: The return value of the executed function, or `None` if no function is stored. If an exception occurs, 
            it returns the exception message as a string.

        Raises:
            Exception: If an error occurs during the function execution, the exception is caught and its message is printed
            if `self.__visibility` is `True`.

        Notes:
            - If `self.__func` is `None`, the method returns `None`.
            - If `self.__args` is `None`, the function is called without arguments.
        """
        try:
            if self.__func and self.__args:
                value = self.__func(*self.__args)
            elif self.__func and not self.__args:
                value = self.__func()
            else:
                value = None
        except Exception as e:
            print(f"Error ocurred:\n{e}") if self.__visibility else None
            return str(e)
        else:
            return value
        
    def _alarm_loop(self, mainPid: int) -> None:
        """
        Run the alarm loop.

        This function monitors the schedules and triggers the alarm at the specified times.
        It suspends and resumes the main process around the execution of the alarm function.

        Args:
            mainPid (int): The process ID of the main process to be monitored.

        Returns:
            None

        Raises:
            ValueError: If `mainPid` is not a valid process ID.

        Notes:
            - The function continuously checks the current time against scheduled alarm times.
            - When the current time matches a scheduled time, the main process is suspended, the alarm function is executed, and then the main process is resumed.
            - If `self.persist` is `False`, the schedule is removed after the alarm is triggered.
            - The function stops running when there are no more schedules or if the main process no longer exists.
        """
        process = psProcess(mainPid)

        while len(self.schedules) > 0 and pid_exists(mainPid):
            now = datetime.now().replace(microsecond=0)
            try:
                idx = self.schedules.index(now)
            except:
                sleep(0.1)
                continue
            else:
                print("Alarm finished!") if self.visibility else None

                process.suspend()
                self.run_function()
                process.resume()

                self.schedules.pop(idx) if not self.persist else None
            
        self.__pid = None
    
    def stop(self) -> None:
        """
        Stop the alarm.

        This method terminates the alarm process if it is currently running. If no alarm is set,
        it raises an error.

        Raises:
            RuntimeError: If no alarm is currently set.

        Notes:
            - The method checks if the alarm process exists and terminates it if so.
            - If `self.visibility` is `True`, it prints a message indicating that the alarm has stopped.
        """
        if self.__pid and pid_exists(self.__pid):
            process = psProcess(self.__pid)
            process.terminate()
            self.__pid = None
        else:
            raise RuntimeError("Alarm not set!")
        
        print("Alarm stopped!") if self.visibility else None

    def get_pid(self) -> int:
        """
        Get the process ID.

        This method returns the process ID of the running alarm process. If no alarm process 
        is running, it raises an error.

        Returns:
            int: The process ID of the running alarm.

        Raises:
            AttributeError: If no alarm process is currently running.

        Notes:
            - The method checks if the alarm process ID is set and if the process exists.
        """
        if not self.__pid or not pid_exists(self.__pid):
            raise AttributeError(f"There is no hourglass running!")
        else:
            return int(self.__pid)

    def is_active(self) -> bool:
        """
        Check if the alarm is active.

        This method checks if the alarm process is currently running.

        Returns:
            bool: `True` if the alarm process is active, `False` otherwise.

        Notes:
            - The method checks if the process ID is set and if the process exists.
        """
        return self.__pid and pid_exists(self.__pid)

if __name__ == "__main__":
    pass