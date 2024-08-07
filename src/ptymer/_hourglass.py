from typing import Callable, Optional, Union
from multiprocessing import Process, Value, freeze_support
from datetime import timedelta
from psutil import Process as psProcess, pid_exists

class HourGlass:
    def __init__(self, 
                 seconds: Union[int, float], 
                 target: Optional[Callable] = None,
                 args: Optional[tuple] = None,
                 visibility: bool = False) -> None:
        """
        Initialize the hourglass timer.

        Args:
            seconds (Union[int, float]): The duration of the timer in seconds. Must be a positive number.
            target (Optional[Callable]): A callable function to be executed when the timer ends. Default is None.
            args (Optional[tuple]): A tuple of arguments to pass to the target function. Default is None.
            visibility (bool): Determines if messages should be displayed. Default is False.

        Raises:
            TypeError: If `visibility` is not a boolean, if `seconds` is not numeric, if `target` is not a callable or if `args` is not a tuple.
            ValueError: If `seconds` is less than 1, or if `args` are defined without a target function.

        Notes:
            - The `visibility` attribute defines if the hourglass will show messages or not.
            - The `seconds` attribute represents the total time of the hourglass.
            - The `__pid` attribute stores the process ID of the hourglass.
            - The `__process` attribute stores the process of the hourglass.
            - The `target` attribute is the function to be executed when the timer ends.
            - The `args` attribute contains the arguments for the `target` function.
        """
        if not isinstance(visibility, bool):
            raise TypeError(f"Visibility must be a boolean! Got {type(visibility)}!") 
        else: self.visibility: bool = visibility
        # Defines if the hourglass will show messages or not

        if not isinstance(seconds, (float, int)):
            raise TypeError(f"Seconds must be numeric! Got {type(seconds)}!")
        elif seconds < 1:
            raise ValueError(f"Seconds must be greater than 1!")
        else: self.__total_time = Value('i', int(seconds), lock=True) if isinstance(seconds, int) else Value('d', float(seconds), lock=True)
        # Total time of the hourglass

        self.__pid: Optional[int] = None
        # Process id of the hourglass

        self.__process: Optional[Process] = None
        # Process of the hourglass

        if target and not isinstance(target, Callable):
            raise TypeError(f"Target must be a function! Got {type(target)}!")
        else: self.target: Callable = target
        # Function to be executed when time is up

        if args and not isinstance(args, tuple):
            raise TypeError(f"Arguments must be a tuple! Got {type(args)}!")
        elif args and not target:
            raise ValueError(f"Arguments cannot be defined without a target function!")
        else: self.args: tuple = args
        # Arguments of the function

    def __str__(self) -> str:
        return f"Class HourGlass()\nVisibility: {self.visibility}\nRemaining time: {self.__total_time.value}\nProcess id: {self.__pid if self.status else None}\nFunction: {self.target}\nArguments: {self.args}\n"
    
    def __eq__(self, other: "HourGlass") -> bool:
        if isinstance(other, HourGlass):
            return self.__total_time.value == other.__total_time.value
        else: raise TypeError(f"Cannot compare HourGlass with {type(other)}!")
    
    def __ne__(self, other: "HourGlass") -> bool:
        if isinstance(other, HourGlass):
            return self.__total_time.value != other.__total_time.value
        else: raise TypeError(f"Cannot compare HourGlass with {type(other)}!")
    
    def __lt__(self, other: "HourGlass") -> bool:
        if isinstance(other, HourGlass):
            return self.__total_time.value < other.__total_time.value
        else: raise TypeError(f"Cannot compare HourGlass with {type(other)}!")

    def __le__(self, other: "HourGlass") -> bool:
        if isinstance(other, HourGlass):
            return self.__total_time.value <= other.__total_time.value
        else: raise TypeError(f"Cannot compare HourGlass with {type(other)}!")

    def __gt__(self, other: "HourGlass") -> bool:
        if isinstance(other, HourGlass):
            return self.__total_time.value > other.__total_time.value
        else: raise TypeError(f"Cannot compare HourGlass with {type(other)}!")

    def __ge__(self, other: "HourGlass") -> bool:
        if isinstance(other, HourGlass):
            return self.__total_time.value >= other.__total_time.value
        else: raise TypeError(f"Cannot compare HourGlass with {type(other)}!")
    
    def __call__(self, seconds: Union[int, float]) -> "HourGlass":
        self.__total_time.value = seconds
        # Change the total time of the hourglass

        return self
    
    @staticmethod
    def _time_format(secs: Union[int, float]) -> timedelta:
        """
        Convert seconds to a `timedelta` object.

        This method takes a number of seconds and converts it to a `timedelta` object, 
        representing the equivalent hours, minutes, and seconds.

        Args:
            secs (Union[int, float]): The number of seconds to convert.

        Returns:
            timedelta: A `timedelta` object representing the equivalent time.

        Raises:
            ValueError: If the provided seconds cannot be converted to a valid time.

        Notes:
            - The input `secs` can be either an integer or a float.
            - The method prints the intermediate time string for debugging purposes.
            - The time is formatted to include hours, minutes, and seconds with two decimal places for seconds.
        """
        mins, secs = divmod(secs, 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)
 
        return timedelta(days=days, hours=hours, minutes=mins, seconds=secs)
    
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
            if `self.visibility` is `True`.

        Notes:
            - If `target` is `None`, the method returns `None`.
            - If `args` is `None`, the function is called without arguments.
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
    
    def _decrease_time(self, mainPid: int) -> None:
        """
        Decrease the timer by 1 second increments.

        This method decreases the timer by 1 second at a time until the timer reaches zero or 
        the main process (identified by `mainPid`) is no longer running. When the timer ends 
        or the main process is interrupted, it runs the specified function and resumes the 
        main process.

        Args:
            mainPid (int): The process ID of the main process.

        Raises:
            Exception: If any error occurs during the process.

        Notes:
            - This method uses `sleep(1)` to wait for 1 second intervals between decreases.
            - If the timer runs out or the main process is interrupted, it prints a message if 
            `self.visibility` is `True`.
            - The method suspends the main process, runs the target function, and then resumes the main process.
        """
        from time import sleep
        try:
            process = psProcess(mainPid)

            while self.__total_time.value > 0:
                self.__total_time.value-=1
                sleep(1)
            # Decrease time in 1 second and sleep for 1 second (main 
            # process is not interrupted)

            print("Time is up!" if pid_exists(mainPid) else "Main process interrupted!") if self.visibility else None 
            
            process.suspend()
            self._run_function(self.target, self.args, self.visibility)
            process.resume()
            # Stop main process, run the function and resume the main process
        except Exception as e:
            print(e) if self.visibility else None
            raise e
    
    def start(self) -> "HourGlass":
        """
        Start the hourglass and return the `HourGlass` object.

        This method initializes and starts the hourglass timer. If an hourglass process is 
        already running, it raises an error. Otherwise, it starts a new process to run the 
        timer in the background.

        Returns:
            HourGlass: The current instance of the `HourGlass` class.

        Raises:
            RuntimeError: If the hourglass is already running.

        Notes:
            - This method uses `freeze_support()` to ensure compatibility with Windows.
            - The hourglass process is started as a daemon process.
            - If `self.visibility` is `True`, it prints a message indicating that the hourglass has started.
        """
        from os import getpid

        freeze_support()
        # Freeze support for Windows

        if self.status:
            raise RuntimeError(f"Hourglass already running!")
        else:
            print("Starting hourglass!") if self.visibility else None

            process = Process(target=self._decrease_time, args=(getpid(),), daemon=True)
            process.start()
            # Start the parallel process

            self.__pid = process.pid
            self.__process = process

            return self
        
    def stop(self) -> None:
        """
        Stop the hourglass.

        This method terminates the running hourglass process. If no hourglass process is running,
        it raises an error.

        Raises:
            AttributeError: If no hourglass process is currently running.

        Notes:
            - The method checks if the hourglass process ID is set and if the process exists.
            - If `self.visibility` is `True`, it prints a message indicating that the hourglass has stopped.
        """
        if not self.status:
            raise RuntimeError(f"There is no hourglass running!")
        else:
            process = psProcess(self.__pid)
            process.terminate()
            self.__pid = None
            self.__process = None
            if self.visibility:
                print("Hourglass stopped!")
    
    @property
    def remaining_time(self) -> timedelta:
        """
        Show the remaining time in `timedelta` format (HH:MM:SS.ms).

        This method returns the remaining time of the hourglass as a `timedelta` object.

        Returns:
            timedelta: The remaining time of the hourglass.

        Notes:
            - The remaining time is formatted as a `timedelta` object.
        """
        val = self._time_format(self.__total_time.value) 
        return val
    
    @property
    def remaining_seconds(self) -> Union[int, float]:
        """
        Show the remaining time in seconds.

        This method returns the remaining time of the hourglass in seconds.

        Returns:
            int | float: The remaining time in seconds.
        """
        return self.__total_time.value

    @property
    def pid(self) -> int:
        """
        Return the process ID of the running hourglass.

        This method returns the process ID of the hourglass if it is currently running. 
        If no hourglass process is running, it raises an error.

        Returns:
            int: The process ID of the running hourglass.

        Raises:
            AttributeError: If no hourglass process is currently running.
        """
        if not self.status:
            raise AttributeError(f"There is no hourglass running!")
        else:
            return int(self.__pid)
    
    @property
    def status(self) -> bool:
        """
        Check if the hourglass is active.

        This method returns a boolean indicating whether the hourglass process is currently 
        active.

        Returns:
            bool: `True` if the hourglass process is active, `False` otherwise.
        """
        if self.__pid and pid_exists(self.__pid):
            return True
        else:
            return False
    
    def wait(self) -> None:
        """
        Wait for the hourglass to finish.

        This method waits for the hourglass process to finish before returning.

        Returns:
            None

        Notes:
            - The method uses the `join()` method of the HourGlass process.
        """
        if self.status:
            self.__process.join()
        else:
            raise RuntimeError("HourGlass not set!")
        
if __name__ == "__main__":
    pass
    