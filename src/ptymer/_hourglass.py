from typing import Callable
from multiprocessing import Process, Value, freeze_support
from datetime import datetime
from psutil import Process as psProcess

class HourGlass:
    def __init__(self, 
                 seconds: int | float, 
                 target: Callable = None,
                 args: tuple = (), 
                 visibility: bool = False,
                 persist: bool = False) -> None:
        freeze_support()
        # Freeze support for Windows

        self.__visibility: bool = visibility
        # Defines if the hourglass will show messages or not

        if seconds > 0: self.__total_time = Value('i', seconds, lock=False)
        else: raise ValueError(f"Seconds must be greater than 0!")
        # Total time of the hourglass

        self.__pid: int | None = None
        # Process id of the hourglass

        self.__func: Callable = target
        # Function to be executed when time is up

        self.__args: tuple = args
        # Arguments of the function

        self.__persist: bool = persist
        # If True, the secondary process will not be interrupted when the main process is interrupted

    def __str__(self) -> str:
        return f"Class HourGlass()\nVisibility: {self.__visibility}\nRemaining time: {self.__total_time.value}\nProcess id: {self.__pid}\nFunction: {self.__func}\nArguments: {self.__args}\nPersist: {self.__persist}\n"
    
    def __eq__(self, other: "HourGlass") -> bool:
        if isinstance(other, HourGlass):
            return self.__total_time.value == other.__total_time.value
    
    def __ne__(self, other: "HourGlass") -> bool:
        if isinstance(other, HourGlass):
            return self.__total_time.value != other.__total_time.value
    
    def __lt__(self, other: "HourGlass") -> bool:
        if isinstance(other, HourGlass):
            return self.__total_time.value < other.__total_time.value
    
    def __le__(self, other: "HourGlass") -> bool:
        if isinstance(other, HourGlass):
            return self.__total_time.value <= other.__total_time.value
    
    def __gt__(self, other: "HourGlass") -> bool:
        if isinstance(other, HourGlass):
            return self.__total_time.value > other.__total_time.value
    
    def __ge__(self, other: "HourGlass") -> bool:
        if isinstance(other, HourGlass):
            return self.__total_time.value >= other.__total_time.value
    
    def __call__(self, seconds: int | float) -> "HourGlass":
        self.__total_time.value = seconds
        # Change the total time of the hourglass

        return self
    
    @staticmethod
    def _time_format(secs: int | float) -> datetime.time:
        """
        Convert seconds to datetime.time
        """
        mins, secs = divmod(secs, 60)
        hours, mins = divmod(mins, 60)
 
        time_str = f"{int(hours)} {int(mins)} {float(secs)}"
        return datetime.strptime(time_str, "%H %M %S.%f").time()
    
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
    
    def _decrease_time(self, mainPid: int) -> None:
        """
        Decrease the time in 1 second
        When it ends, it runs the chosen function
        It also interrupts main executin though the mainPid
        """
        from time import sleep
        from psutil import pid_exists

        process = psProcess(mainPid)

        try:
            while self.__total_time.value > 0 and (pid_exists(mainPid) or self.__persist):
                self.__total_time.value-=1
                sleep(1)
            # Decrease time in 1 second and sleep for 1 second (main 
            # process is not interrupted)

            print("Time is up!" if pid_exists(mainPid) else "Main process interrupted!") if self.__visibility else None 
            
            process.suspend()
            self.run_function(self.__func, *self.__args)
            process.resume()
            # Stop main process, run the function and resume the main process

        except:
            pass
    
    def start(self) -> "HourGlass":
        """
        Start the hourglass and return the self object
        """
        from os import getpid

        if self.__pid:
            raise RuntimeError(f"Hourglass already running!")
        else:
            print("Starting hourglass!") if self.__visibility else None

            process = Process(target=self._decrease_time, args=(getpid(),))
            process.start()
            # Start the parallel process

            self.__pid = process.pid

            return self
        
    def stop(self) -> None:
        """
        Stop the hourglass
        """
        if not self.__pid:
            raise AttributeError(f"There is no hourglass running!")
        else:
            process = psProcess(self.__pid)
            process.terminate()
            self.__pid = None
            if self.__visibility:
                print("Hourglass stopped!")
    
    def show(self) -> None:
        """
        Show the remaining time in str format (HH:MM:SS.ms)
        """
        print(f"Remaining time: {str(self._time_format(self.__total_time.value))}")
    
    def get_pid(self) -> int:
        """
        Return the process id
        """
        if not self.__pid:
            raise AttributeError(f"There is no hourglass running!")
        else:
            return int(self.__pid)
    