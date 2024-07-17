from datetime import datetime
from contextlib import ContextDecorator
from typing import Optional, Union, Dict, Tuple

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
            - Raises an error if `visibility` is not a boolean.
        """
        self.__start_time: Optional[datetime] = None
        self.__marks: list[list[str, ]] = []
        if not isinstance(visibility, bool):
            raise TypeError("Visibility must be a boolean!")
        else: self.__visibility: bool = visibility

    def __str__(self) -> str:
        return f"Class Timer()\nVisibility: {self.__visibility}\nStatus: {'on' if self.__start_time else 'off'}\nStart time: {str(self.__start_time)}\nTime since start: {str(self.current_time())}\nQuantity of marks: {len(self.__marks)}\n"
    
    def __enter__(self) -> "Timer":
        """
        Start a new timer as a context manager.

        Raises:
            RuntimeError: If the timer is already executing.

        Returns:
            Timer: The Timer instance itself.
        """
        if self.__start_time:
            raise RuntimeError(f"Timer already executing!")
        else:
            self.start()
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
        if not self.__start_time:
            raise AttributeError(f"There is no timer executing!")
        elif exc_type:
            raise exc_type(exc_value)
        else:
            self.stop()
        
    def __eq__(self, other: "Timer") -> bool:
        if isinstance(other, Timer):
            return self.__start_time == other.__start_time
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
        print(time_str)
        return datetime.strptime(time_str, "%H %M %S.%f").time()
        
    def start(self) -> datetime.time:
        """
        Start the timer and set the start time.

        Returns:
            datetime.time: The start time of the timer as a `datetime.time` object.

        Raises:
            RuntimeError: If the timer is already executing.

        Notes:
            - Sets `self.__start_time` to the current timestamp using `datetime.now()`.
            - If `self.__visibility` is `True`, prints the formatted start time using `_time_format(0)`.
        """
        if self.__start_time:
            raise RuntimeError(f"Timer already executing!")
        else:
            self.__start_time = datetime.now()
            print(f"Starttime: {str(self._time_format(0))}") if self.__visibility else None
            return self
    
    def stop(self) -> datetime.time:
        """
        Stop the timer and set the end time.

        Returns:
            datetime.time: The end time of the timer as a `datetime.time` object.

        Raises:
            AttributeError: If there is no timer currently executing.

        Notes:
            - Calculates the end time using the difference between the current time and `self.__start_time`.
            - Resets `self.__start_time` to `None` after stopping the timer.
            - If `self.__visibility` is `True`, prints the formatted end time and lists any recorded marks.
        """
        if not self.__start_time:
            raise AttributeError(f"There is no timer executing!")
        else:
            end_time = self._time_format((datetime.now() - self.__start_time).total_seconds())
            self.__start_time = None

            if self.__visibility:
                print(f"Endtime: {str(end_time)}")
                if len(self.__marks) > 0:
                    print("Marks:")
                    self.list_marks()

            return end_time
        
    def restart(self) -> None:
        """
        Restart the timer with a new start time and clean the marks.

        Raises:
            RuntimeError: If there is no timer currently running.

        Notes:
            - Updates `self.__start_time` to the current timestamp using `datetime.now()`.
            - Resets `self.__marks` to an empty list.
            - If `self.__visibility` is `True`, prints the timestamp of the restart.
        """
        if not self.__start_time:
            raise RuntimeError(f"There is no timer running!")
        else:
            now = datetime.now()
            if self.__visibility:
                print(f"Restarting point: {now}")
            self.__start_time = now
            self.__marks = []
    
    def current_time(self) -> datetime.time:
        """
        Return the current elapsed time of the timer from the start time.

        Returns:
            datetime.time: The current elapsed time in `HH:MM:SS.ms` format.

        Raises:
            AttributeError: If there is no timer currently executing.

        Notes:
            - Calculates the elapsed time from `self.__start_time` to the current time.
            - Returns the formatted time using `_time_format` method.
        """
        if not self.__start_time:
            raise AttributeError(f"There is no timer executing!")
        else:
            return self._time_format((datetime.now() - self.__start_time).total_seconds())
    
    def mark(self, observ: Optional[str] = None) -> None:
        """
        Create a mark with the current time and an optional observation.

        Args:
            observ (str, optional): An optional observation associated with the mark.

        Raises:
            AttributeError: If there is no timer currently executing.

        Notes:
            - Adds a new mark to `self.__marks` consisting of the current time and the observation.
            - If `self.__visibility` is `True`, prints the mark number, current time, and observation.
        """
        if not self.__start_time:
            raise AttributeError(f"There is no timer executing!")
        else:
            if self.__visibility:
                print(f"Mark {len(self.__marks)+1}: {str(self.current_time())}" + "\t" + f"{(observ) if observ else ''}")
            self.__marks.append([self.current_time(), observ if observ else ""])

    def list_marks(self) -> Dict[int, Tuple[str, datetime.time]]:
        """
        Return a dictionary with the marks and their respective times.

        Returns:
            Dict[int, Tuple[str, datetime.time]]: A dictionary where keys are mark indices 
            and values are tuples containing the observation (if any) and the mark time.

        Raises:
            AttributeError: If there are no marks to show.

        Notes:
            - If `self.__visibility` is `True`, prints each mark with its index, observation, and time.
            - Returns a dictionary representation of `self.__marks` where each entry contains the 
            mark index as key and a tuple of observation (or empty string) and mark time.
        """
        if self.__marks == []:
            raise AttributeError(f"There are no marks to show!")
        elif self.__visibility:
            [print(f"{x+1}: {mark[0]}" + "\t" + f"{mark[1]}") for x, mark in enumerate(self.__marks)]
        return {idx: (sublist[0], sublist[1]) for idx, sublist in enumerate(self.__marks)}
    
    def show(self) -> None:
        """
        Print the current elapsed time of the timer in `HH:MM:SS.ms` format.

        Notes:
            - Uses the `current_time` method to retrieve and format the current elapsed time.
            - Prints the formatted current time with a descriptive label.
        """
        print(f"Current time: {str(self.current_time())}")

if __name__ == "__main__":
    pass