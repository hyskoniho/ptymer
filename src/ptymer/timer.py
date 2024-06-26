from datetime import datetime, timedelta
from time import sleep

class Timer:
    def __init__(self):
        self.__start_time: datetime | None = None
        self.__end_time: datetime | None = None
        self._marks: list[list[str, ]] = []
        self.__running: bool = False
    
    @staticmethod
    def _time_format(secs: int | float) -> datetime.time:
        """
        Convert seconds to datetime.time
        """
        mins, secs = divmod(secs, 60)
        hours, mins = divmod(mins, 60)

        time_str = f"{int(hours)} {int(mins)} {secs}"
        return datetime.strptime(time_str, "%H %M %S.%f").time()
        
    def start(self) -> None:
        """
        Starts the timer and sets the start time
        """
        if self.__running:
            raise RuntimeError(f"Timer already executing!")
        else:
            self.__running = True 
            self.__start_time = datetime.now()
    
    def stop(self, show: bool = False) -> str:
        """
        Stop the timer and sets the end time
        It can show the endpoint and the list of marks
        """
        if not self.__running:
            raise AttributeError(f"There is no timer executing!")
        else:
            self.__running = False
            self.__end_time = self._time_format((datetime.now() - self.__start_time).total_seconds())

            print(f"Endpoint: {self.__end_time}") if show else None
            [print(f"Mark {x+1}: {mark[0]}{(" \t '" + str(mark[1]) + "'") if mark[1] != "" else ""}") for x, mark in enumerate(self._marks)] if show and len(self._marks) > 0 else None
            return str(self.__end_time)
    
    def current_time(self) -> datetime.time:
        """
        Return current time of the timer from the start time in datetime format
        """
        if not self.__running:
            raise AttributeError(f"There is no timer executing!")
        else:
            return self._time_format((datetime.now() - self.__start_time).total_seconds())
    
    def mark(self, observ: None | str = None) -> None:
        """
        Create a mark with the current time and an observation (optional)
        """
        self._marks.append([self.current_time(), f"{observ}" if observ else ""])

    def list_marks(self):
        """
        Returns a dictionary with the marks and their respective times
        """
        if self._marks == []:
            raise AttributeError(f"There are no marks to show!")
        return {idx: (sublist[0], sublist[1]) for idx, sublist in enumerate(self._marks)}
    
    def show(self):
        """
        Show the current time
        """
        print(f"Current time: {str(self.current_time())}")
    
    def restart(self):
        """
        Restart the timer
        """
        if not self.__running:
            raise RuntimeError(f"There is no timer running!")
        else:
            self.__start_time = datetime.now()
            self._marks = []

class HourGlass():
    def __init__(self):
        self.__start_time: None = None
        self.__running: bool = False
    

if __name__ == '__main__':
    timer = Timer()
    timer2 = Timer()
    timer.start()

    sleep(3)

    timer.mark("Primeiro marco")
    sleep(0.1)
    timer.mark()
    timer2.start()
    sleep(0.1)
    timer.mark(" Segundo marco")
    sleep(0.1)
    timer.mark()
    timer2.mark()
    sleep(0.1)
    print(timer.current_time())

    sleep(3)
    timer.mark("     Terceiro marco")
    sleep(5)
    timer.mark()
    timer2.stop(True)
    print(timer.list_marks())
    sleep(1)

    timer.stop(True)