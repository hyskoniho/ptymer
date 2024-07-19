from datetime import datetime
from typing import Callable, Any, List, Tuple, Union, Optional
from dataclasses import dataclass
from dateutil import parser
from psutil import Process as psProcess, pid_exists
from multiprocessing import Process, freeze_support

@dataclass
class Alarm():
    schedules: List[Union[datetime, str, Tuple[int, int, int, int, int, int, int]]]
    # list of datetime objects
    target: Optional[Callable] = None
    # function that will be executed when the alarm is triggered
    args: Optional[Tuple[Any]] = None
    # arguments of the function
    visibility: bool = False
    # defines if the alarm will show messages or not
    keep_schedules: bool = False
    # if true, the alarm will not be elimnated after being triggered
    __pid: Optional[int] = None
    # process id of the alarm
    __process: Optional[Process] = None
    # process object of the alarm

    def __post_init__(self) -> None:
        """
        Post-initialization method.

        This method validates the attributes and converts string representations of dates 
        to `datetime` objects. It ensures that the schedules, target function, arguments, 
        and other attributes are correctly defined and of the proper types.

        Raises:
            TypeError: If `schedules` is not a list, if `target` is not a callable function, 
                    if `args` is not a tuple, if `visibility` is not a boolean, if `keep_schedules` 
                    is not a boolean, or if any schedule entry is not a valid date.
            ValueError: If `schedules` is empty, if `target` is not defined, or if `args` 
                        are defined without a target function.

        Notes:
            - `schedules` should be a list of dates in `datetime`, `tuple`, or `str` format.
            - `target` should be a callable function.
            - `args` should be a tuple of arguments for the target function.
            - `visibility` and `keep_schedules` should be boolean values.
            - The method converts string dates to `datetime` objects and tuple dates to 
            `datetime` objects, truncating microseconds for `datetime` objects.
        """
        if not isinstance(self.schedules, list):
            raise TypeError("Schedules must be a list!")
        elif not self.schedules:
            raise ValueError("Schedules must be defined!")
        elif self.target and not isinstance(self.target, Callable):
            raise TypeError("Target must be a function!")
        elif self.args and not isinstance(self.args, tuple):
            raise TypeError("Arguments must be a tuple!")
        elif self.args and not self.target:
            raise ValueError(f"Arguments cannot be defined without a target function!")
        elif not isinstance(self.visibility, bool):
            raise TypeError("Visibility must be a boolean!")
        elif not isinstance(self.keep_schedules, bool):
            raise TypeError("keep_schedules must be a boolean!")
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
        return f"Class Alarm()\nVisibility: {self.visibility}\nSchedules: {self.args}\nKeep_schedules: {self.keep_schedules}\nProcess id: {self.__pid if self.status else None}"
    
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

        if self.status:
            raise ValueError("Alarm already set!")
        else:
            process = Process(target=self._alarm_loop, args=(getpid(),), daemon=True)
            process.start()
            self.__pid = process.pid
            self.__process = process
            
            print("Alarm started!") if self.visibility else None
            return self
        
    @staticmethod
    def _run_function(target, args, visibility) -> any:
        """
        Execute the stored function with its arguments.

        This method attempts to run the function stored in `self.target` with the arguments stored in `self.args`.
        If no arguments are provided, the function is called without arguments.

        Returns:
            any: The return value of the executed function, or `None` if no function is stored. If an exception occurs, 
            it returns the exception message as a string.

        Raises:
            Exception: If an error occurs during the function execution, the exception is caught and its message is printed

        Notes:
            - If `self.target` is `None`, the method returns `None`.
            - If `self.args` is `None`, the function is called without arguments.
        """
        try:
            if target and args:
                value = target(*args)
            elif target and not args:
                value = target()
            else:
                value = None
        except Exception as e:
            print(f"Error ocurred:\n{e}")
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
            - If `self.keep_schedules` is `False`, the schedule is removed after the alarm is triggered.
            - The function stops running when there are no more schedules or if the main process no longer exists.
        """
        process = psProcess(mainPid)
        lastIdx = None

        while len(self.schedules) > 0:
            now = datetime.now().replace(microsecond=0)
            try:
                idx = self.schedules.index(now)
            except:
                continue # if the current time is not in the schedules, it continues the loop
            else:
                if idx != lastIdx: # this is due the speed of the loop, sometimes it triggers the same alarm twice (or much more)
                    print("Alarm triggered!") if self.visibility else None

                    process.suspend()
                    self.run_function()
                    process.resume()

                    lastIdx = idx
                    if not self.keep_schedules:
                        self.schedules.pop(idx)  
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
        if self.status:
            process = psProcess(self.__pid)
            process.terminate()
            self.__pid = None
            self.__process = None
        else:
            raise RuntimeError("Alarm not set!")
        
        print("Alarm stopped!") if self.visibility else None

    @property
    def pid(self) -> int:
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
        if not self.status:
            raise AttributeError(f"There is no hourglass running!")
        else:
            return int(self.__pid)

    @property
    def status(self) -> bool:
        """
        Check if the alarm is active.

        This method checks if the alarm process is currently running.

        Returns:
            bool: `True` if the alarm process is active, `False` otherwise.

        Notes:
            - The method checks if the process ID is set and if the process exists.
        """
        return self.__pid and pid_exists(self.__pid)

    def wait(self) -> None:
        """
        Wait for the alarm to finish.

        This method waits for the alarm process to finish before returning.

        Returns:
            None

        Notes:
            - The method uses the `join()` method of the alarm process.
        """
        if self.status:
            self.__process.join()
        else:
            raise RuntimeError("Alarm not set!")
        
if __name__ == "__main__":
    pass