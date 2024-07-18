from typing import Callable, Optional, Union
from multiprocessing import Process, Value, freeze_support
from datetime import datetime
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
            raise TypeError(f"Visibility must be a boolean! Got {type(self.__visibility)}!") 
        else: self.__visibility: bool = visibility
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
        else: self.__func: Callable = target
        # Function to be executed when time is up

        if args and not isinstance(args, tuple):
            raise TypeError(f"Arguments must be a tuple! Got {type(args)}!")
        elif args and not target:
            raise ValueError(f"Arguments cannot be defined without a target function!")
        else: self.__args: tuple = args
        # Arguments of the function

    def __str__(self) -> str:
        return f"Class HourGlass()\nVisibility: {self.__visibility}\nRemaining time: {self.__total_time.value}\nProcess id: {self.__pid if self.is_active() else None}\nFunction: {self.__func}\nArguments: {self.__args}\n"
    
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
    def _time_format(secs: Union[int, float]) -> datetime.time:
        """
        Convert seconds to a `datetime.time` object.

        This method takes a number of seconds and converts it to a `datetime.time` object, 
        representing the equivalent hours, minutes, and seconds.

        Args:
            secs (Union[int, float]): The number of seconds to convert.

        Returns:
            datetime.time: A `datetime.time` object representing the equivalent time.

        Raises:
            ValueError: If the provided seconds cannot be converted to a valid time.

        Notes:
            - The input `secs` can be either an integer or a float.
            - The method prints the intermediate time string for debugging purposes.
            - The time is formatted to include hours, minutes, and seconds with two decimal places for seconds.
        """
        mins, secs = divmod(secs, 60)
        hours, mins = divmod(mins, 60)
 
        time_str = f"{int(hours)} {int(mins)} {float(secs):.2f}"
        return datetime.strptime(time_str, "%H %M %S.%f").time()
    
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
            `self.__visibility` is `True`.
            - The method suspends the main process, runs the target function, and then resumes the main process.
        """
        from time import sleep

        process = psProcess(mainPid)

        try:
            while self.__total_time.value > 0 and pid_exists(mainPid):
                self.__total_time.value-=1
                sleep(1)
            # Decrease time in 1 second and sleep for 1 second (main 
            # process is not interrupted)

            print("Time is up!" if pid_exists(mainPid) else "Main process interrupted!") if self.__visibility else None 
            
            process.suspend()
            self.run_function()
            process.resume()
            # Stop main process, run the function and resume the main process
        except Exception as e:
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
            - If `self.__visibility` is `True`, it prints a message indicating that the hourglass has started.
        """
        from os import getpid

        freeze_support()
        # Freeze support for Windows

        if self.is_active():
            raise RuntimeError(f"Hourglass already running!")
        else:
            print("Starting hourglass!") if self.__visibility else None

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
            - If `self.__visibility` is `True`, it prints a message indicating that the hourglass has stopped.
        """
        if not self.is_active():
            raise AttributeError(f"There is no hourglass running!")
        else:
            process = psProcess(self.__pid)
            process.terminate()
            self.__pid = None
            self.__process = None
            if self.__visibility:
                print("Hourglass stopped!")
    
    def remaining_time(self) -> datetime.time:
        """
        Show the remaining time in `datetime.time` format (HH:MM:SS.ms).

        This method returns the remaining time of the hourglass as a `datetime.time` object.
        If no hourglass process is running, it raises an error.

        Returns:
            datetime.time: The remaining time of the hourglass.

        Raises:
            AttributeError: If no hourglass process is currently running.

        Notes:
            - If `self.__visibility` is `True`, it prints the remaining time.
            - The remaining time is formatted as a `datetime.time` object.
        """
        if not self.is_active():
            raise AttributeError(f"There is no hourglass running!")
        else:
            val = self._time_format(self.__total_time.value)
            print(f"Remaining time: {str(val)}") if self.__visibility else None  
            return val
    
    def remaining_seconds(self) -> int:
        """
        Show the remaining time in seconds.

        This method returns the remaining time of the hourglass in seconds. If no hourglass 
        process is running, it raises an error.

        Returns:
            int: The remaining time in seconds.

        Raises:
            AttributeError: If no hourglass process is currently running.

        Notes:
            - If `self.__visibility` is `True`, it prints the remaining seconds.
            - The method converts the remaining time from a `datetime.time` object to seconds.
        """
        if not self.is_active():
            raise AttributeError(f"There is no hourglass running!")
        else:
            dateobj = self._time_format(self.__total_time.value)

            total = int(dateobj.strftime('%S'))
            total += int(dateobj.strftime('%M')) * 60
            total += int(dateobj.strftime('%H')) * 60 * 60
            print(f"Remaining seconds: {total}") if self.__visibility else None
            return total

    def get_pid(self) -> int:
        """
        Return the process ID of the running hourglass.

        This method returns the process ID of the hourglass if it is currently running. 
        If no hourglass process is running, it raises an error.

        Returns:
            int: The process ID of the running hourglass.

        Raises:
            AttributeError: If no hourglass process is currently running.
        """
        if not self.is_active():
            raise AttributeError(f"There is no hourglass running!")
        else:
            return int(self.__pid)
    
    def is_active(self) -> bool:
        """
        Check if the hourglass is active.

        This method returns a boolean indicating whether the hourglass process is currently 
        active.

        Returns:
            bool: `True` if the hourglass process is active, `False` otherwise.
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
        if self.is_active():
            self.__process.join()
        else:
            raise RuntimeError("Alarm not set!")
        
if __name__ == "__main__":
    pass
    