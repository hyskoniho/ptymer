from datetime import datetime, timedelta
from contextlib import ContextDecorator
from typing import Optional, Dict, Tuple

class Timer(ContextDecorator):
    def __init__(self, visibility: bool = False) -> None:
        """
        Initialize a Timer instance.

        Args:
            visibility (bool, optional): Determines if messages will be displayed. Defaults to False.

        Raises:
            TypeError: If visibility is not a boolean.

        Notes:
            - Initializes `self.__start_time` as `None`.
            - Initializes `self.__marks` as an empty list of lists.
            - Initializes `self.__depth_meter` as 0.
            - Raises an error if `visibility` is not a boolean.
        """
        self.__start_time: Optional[datetime] = None
        self.__marks: list[list[timedelta, Optional[str]]] = []
        self.__depth_meter: int = 0

        if not isinstance(visibility, bool):
            raise TypeError("Visibility must be a boolean!")
        else: self.visibility: bool = visibility

    def __str__(self) -> str:
        return f"Class Timer()\nVisibility: {self.visibility}\nActive: {self.status}\nStart time: {str(self.__start_time)}\nTime since start: {str(self.current_time)}\nQuantity of marks: {len(self.__marks)}\n"
    
    def __enter__(self) -> "Timer":
        """
        Start a new timer as a context manager.

        Returns:
            Timer: The Timer instance itself.
        
        Notes:
            - Checks the depth of the recursion and starts the timer if it is the first call.
        """
        if self.__depth_meter == 0:
            self.start()
        self.__depth_meter += 1
        return self

    def __exit__(self, exc_type: Optional[Exception], exc_value: Optional[str], traceback: str) -> None:
        """
        Stop the context manager timer.

        Args:
            exc_type (Optional[Exception]): The type of exception that occurred, if any.
            exc_value (Optional[str]): The value of the exception message, if any.
            traceback (str): The traceback information.

        Raises:
            AttributeError: If there is no timer currently executing.
            Exception: If `exc_type` is provided, raises the original exception.

        Notes:
            - If no exception occurred (`exc_type` is `None`), the timer is stopped.
        """
        self.__depth_meter -= 1
        if self.__depth_meter == 0:
            if not self.status:
                raise AttributeError("There is no timer executing!")
            else:
                self.stop()
        elif self.__depth_meter < 0 and self.visibility:
            print('Warning: Timer was stopped more times than it was started!')
        if exc_type:
            raise exc_type(exc_value).with_traceback(traceback)
        
    def __eq__(self, other: "Timer") -> bool:
        if isinstance(other, Timer):
            return abs(other.__start_time - self.__start_time) < timedelta(microseconds=100000)
        else: raise TypeError(f"Cannot compare HourGlass with {type(other)}!")

    def __ne__(self, other: "Timer") -> bool:
        if isinstance(other, Timer):
            return self.__start_time != other.__start_time
        else: raise TypeError(f"Cannot compare HourGlass with {type(other)}!")
    
    def __lt__(self, other: "Timer") -> bool:
        if isinstance(other, Timer):
            return self.__start_time < other.__start_time
        else: raise TypeError(f"Cannot compare HourGlass with {type(other)}!")
    
    def __le__(self, other: "Timer") -> bool:
        if isinstance(other, Timer):
            return self.__start_time <= other.__start_time
        else: raise TypeError(f"Cannot compare HourGlass with {type(other)}!")
    
    def __gt__(self, other: "Timer") -> bool:
        if isinstance(other, Timer):
            return self.__start_time > other.__start_time
        else: raise TypeError(f"Cannot compare HourGlass with {type(other)}!")
    
    def __ge__(self, other: "Timer") -> bool:
        if isinstance(other, Timer):
            return self.__start_time >= other.__start_time
        else: raise TypeError(f"Cannot compare HourGlass with {type(other)}!")
        
    def start(self) -> "Timer":
        """
        Start the timer and set the start time.

        Returns:
            Timer: The current instance of the `Timer` class

        Raises:
            RuntimeError: If the timer is already executing.

        Notes:
            - Sets `self.__start_time` to the current timestamp using `datetime.now()`.
        """
        if self.status:
            raise RuntimeError(f"Timer already executing!")
        else:
            self.__start_time = datetime.now()
            print(f"Starting timer at {str(self.__start_time)}!") if self.visibility else None
            return self
    
    def stop(self) -> timedelta:
        """
        Stop the timer and set the end time.

        Returns:
            timedelta: The end time of the timer as a `timedelta` object.

        Raises:
            AttributeError: If there is no timer currently executing.

        Notes:
            - Calculates the end time using the difference between the current time and `self.__start_time`.
            - Resets `self.__start_time` to `None` after stopping the timer.
            - If `self.visibility` is `True`, prints the formatted end time and lists any recorded marks.
        """
        if not self.status:
            raise RuntimeError(f"There is no timer executing!")
        else:
            end_time = datetime.now() - self.__start_time
            self.__start_time = None

            if self.visibility:
                print(f"Total elapsed time: {str(end_time)}")
                if len(self.__marks) > 0:
                    print("Marks:")
                    [print(f"{x+1}: {mark[0]}"  + "\t" + f"{mark[1]}") for x, mark in enumerate(self.__marks)]

            self.__depth_meter = 0 # Reset the depth meter, for the case of using the timer as a context manager and it was stopped before the end of the block for some dark reason
            return end_time
        
    def restart(self) -> None:
        """
        Restart the timer with a new start time and clean the marks.

        Raises:
            RuntimeError: If there is no timer currently running.

        Notes:
            - Updates `self.__start_time` to the current timestamp using `datetime.now()`.
            - Resets `self.__marks` to an empty list.
            - If `self.visibility` is `True`, prints the restart message.
        """
        if not self.status:
            raise RuntimeError(f"There is no timer executing!")
        else:
            now = datetime.now()
            if self.visibility:
                print(f"Restarting timer!")
            self.__start_time = now
            self.__marks = []
    
    @property
    def current_time(self) -> timedelta:
        """
        Return the current elapsed time of the timer from the start time.

        Returns:
            timedelta: The current elapsed time in `HH:MM:SS.ms` format.

        Raises:
            RuntimeError: If there is no timer currently executing.

        Notes:
            - Calculates the elapsed time from `self.__start_time` to the current time.
            - Returns the formatted time using `_time_format` method.
        """
        if not self.status:
            raise RuntimeError(f"There is no timer executing!")
        else:
            return datetime.now() - self.__start_time
    
    def mark(self, observ: Optional[str] = None) -> None:
        """
        Create a mark with the current time and an optional observation.

        Args:
            observ (str, optional): An optional observation associated with the mark.

        Raises:
            RuntimeError: If there is no timer currently executing.

        Notes:
            - Adds a new mark to `self.__marks` consisting of the current time and the observation.
            - If `self.visibility` is `True`, prints the mark number, current time, and observation.
        """
        if not self.status:
            raise RuntimeError(f"There is no timer executing!")
        else:
            if self.visibility:
                print(f"Mark {len(self.__marks)+1}! \nCurrent time: {str(self.current_time)} \nTime since the beginning: \t{str(self.current_time)}" + (f"\nTime since previous mark: \t{self.current_time-self.__marks[-1][0]}" if len(self.__marks) > 0 else "") + (f"\nObs: {observ}" if observ else ""))
            self.__marks.append([self.current_time, observ if observ else ""])

    @property
    def marks(self) -> Dict[int, Tuple[str, timedelta]]:
        """
        Return a dictionary with the marks and their respective times.

        Returns:
            Dict[int, Tuple[str, timedelta]]: A dictionary where keys are mark indices 
            and values are tuples containing the observation (if any) and the mark time.

        Raises:
            AttributeError: If there are no marks to show.

        Notes:
            - Returns a dictionary representation of `self.__marks` where each entry contains the 
            mark index as key and a tuple of mark time and observation (or empty string).
        """
        if self.__marks == []:
            raise AttributeError(f"There are no marks to show!")
        return {idx: [sublist[0], sublist[1]] for idx, sublist in enumerate(self.__marks)}

    @property
    def status(self) -> bool:
        """
        Check if the timer is active.

        This method returns a boolean indicating whether the timer is currently 
        running.

        Returns:
            bool: `True` if the timer is active, `False` otherwise.
        """
        return self.__start_time is not None

if __name__ == "__main__":
    pass