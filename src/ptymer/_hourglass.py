from typing import Callable, Optional, Union
from multiprocessing import Process, Value, freeze_support
from datetime import datetime
from psutil import Process as psProcess, pid_exists

class HourGlass:
    def __init__(self, 
                 seconds: Union[int, float], 
                 target: Optional[Callable] = None,
                 args: Optional[tuple] = None,
                 visibility: bool = False,
                 persist: bool = False) -> None:
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

        if not isinstance(persist, bool):
            raise TypeError(f"Persist must be a boolean! Got {type(persist)}!")
        else: self.__persist: bool = persist
        # If True, the secondary process will not be interrupted when the main process is interrupted 

    def __str__(self) -> str:
        return f"Class HourGlass()\nVisibility: {self.__visibility}\nRemaining time: {self.__total_time.value}\nProcess id: {self.__pid if self.__pid and pid_exists(self.__pid) else None}\nFunction: {self.__func}\nArguments: {self.__args}\nPersist: {self.__persist}\n"
    
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
        Convert seconds to datetime.time
        """
        mins, secs = divmod(secs, 60)
        hours, mins = divmod(mins, 60)
 
        time_str = f"{int(hours)} {int(mins)} {float(secs):.2f}"
        print(time_str)
        return datetime.strptime(time_str, "%H %M %S.%f").time()
    
    def run_function(self) -> any:
        """
        Run a function with arguments
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
        Decrease the time in 1 second
        When it ends, it runs the chosen function
        It also interrupts main executin though the mainPid
        """
        from time import sleep

        process = psProcess(mainPid)

        try:
            while self.__total_time.value > 0 and (pid_exists(mainPid) or self.__persist):
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
        Start the hourglass and return the self object
        """
        from os import getpid

        freeze_support()
        # Freeze support for Windows

        if self.__pid and pid_exists(self.__pid):
            raise RuntimeError(f"Hourglass already running!")
        else:
            print("Starting hourglass!") if self.__visibility else None

            process = Process(target=self._decrease_time, args=(getpid(),), daemon=True)
            process.start()
            # Start the parallel process

            self.__pid = process.pid

            return self
        
    def stop(self) -> None:
        """
        Stop the hourglass
        """
        if not self.__pid or not pid_exists(self.__pid):
            raise AttributeError(f"There is no hourglass running!")
        else:
            process = psProcess(self.__pid)
            process.terminate()
            self.__pid = None
            if self.__visibility:
                print("Hourglass stopped!")
    
    def remaining_time(self) -> datetime.time:
        """
        Show the remaining time in str format (HH:MM:SS.ms)
        """
        if not self.__pid or not pid_exists(self.__pid):
            raise AttributeError(f"There is no hourglass running!")
        else:
            val = self._time_format(self.__total_time.value)
            print(f"Remaining time: {str(val)}") if self.__visibility else None  
            return val
    
    def remaining_seconds(self) -> int:
        """
        Show the remaining time in int (seconds)
        """
        if not self.__pid or not pid_exists(self.__pid):
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
        Return the process id
        """
        if not self.__pid or not pid_exists(self.__pid):
            raise AttributeError(f"There is no hourglass running!")
        else:
            return int(self.__pid)
    
    def is_active(self) -> bool:
        """
        Check if the alarm is active
        """
        return self.__pid and pid_exists(self.__pid)
        
if __name__ == "__main__":
    pass
    