from datetime import datetime
from contextlib import ContextDecorator
from typing import Optional, Union, Dict, Tuple

class Timer(ContextDecorator):
    def __init__(self, visibility: bool = False) -> None:
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
        """
        if self.__start_time:
            raise RuntimeError(f"Timer already executing!")
        else:
            self.start()
        return self

    def __exit__(self, exc_type: Optional[Exception], exc_value: Optional[str], traceback: str) -> None:
        """
        Stop the context manager timer.
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
        Convert seconds to datetime.time
        """
        mins, secs = divmod(secs, 60)
        hours, mins = divmod(mins, 60)

        time_str = f"{int(hours)} {int(mins)} {float(secs)}"
        return datetime.strptime(time_str, "%H %M %S.%f").time()
        
    def start(self) -> datetime.time:
        """
        Starts the timer and sets the start time
        """
        if self.__start_time:
            raise RuntimeError(f"Timer already executing!")
        else:
            self.__start_time = datetime.now()
            print(f"Starttime: {str(self._time_format(0))}") if self.__visibility else None
            return self
    
    def stop(self) -> datetime.time:
        """
        Stop the timer and sets the end time
        It can show the endpoint and the list of marks
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
        Restart the timer, getting a new start time and cleaning the marks
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
        Return current time of the timer from the start time in datetime format
        """
        if not self.__start_time:
            raise AttributeError(f"There is no timer executing!")
        else:
            return self._time_format((datetime.now() - self.__start_time).total_seconds())
    
    def mark(self, observ: Optional[str] = None) -> None:
        """
        Create a mark with the current time and an observation (optional)
        """
        if not self.__start_time:
            raise AttributeError(f"There is no timer executing!")
        else:
            if self.__visibility:
                print(f"Mark {len(self.__marks)+1}: {str(self.current_time())}" + "\t" + f"{(observ) if observ else ''}")
            self.__marks.append([self.current_time(), observ if observ else ""])

    def list_marks(self) -> Dict[int, Tuple[str, datetime.time]]:
        """
        Returns a dictionary with the marks and their respective times
        """
        if self.__marks == []:
            raise AttributeError(f"There are no marks to show!")
        elif self.__visibility:
            [print(f"{x+1}: {mark[0]}" + "\t" + f"{mark[1]}") for x, mark in enumerate(self.__marks)]
        return {idx: (sublist[0], sublist[1]) for idx, sublist in enumerate(self.__marks)}
    
    def show(self) -> None:
        """
        Show the current time in str format (HH:MM:SS.ms)
        """
        print(f"Current time: {str(self.current_time())}")

if __name__ == "__main__":
    pass