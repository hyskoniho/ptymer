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
        mins, secs = divmod(secs, 60)
        horas, mins = divmod(mins, 60)

        time_str = f"{int(horas)} {int(mins)} {secs}"
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
        Para o timer e pode retornar o tempo restante no seguinte 
        formato: HH:MM:SS.ms
        """
        if not self.__running:
            raise AttributeError(f"There is no timer executing!")
        else:
            self.__running = False
            self.__end_time = self._time_format((datetime.now() - self.__start_time).total_seconds())

            print(f"Endpoint: {self.__end_time}") if show else None
            [print(f"Mark {x+1}: {mark[0]}{(" \t '" + mark[1] + "'") if mark[1] != "" else ""}") for x, mark in enumerate(self._marks)] if show and len(self._marks) > 0 else None
            return str(self.__end_time)
    
    def _current_time(self) -> datetime.time:
        """
        Exibe o tempo restante do timer no formato HH:MM:SS.ms
        """
        if not self.__running:
            raise AttributeError(f"There is no timer executing!")
        else:
            return self._time_format((datetime.now() - self.__start_time).total_seconds())
    
    def mark(self, observ: None | str = None) -> None:
        """
        Marca o tempo atual do timer
        """
        self._marks.append([self._current_time(), f"{observ}" if observ else ""])

    def list_marks(self):
        """
        Retorna uma lista com os marcos do timer
        """
        if self._marks == []:
            raise AttributeError(f"There are no marks to show!")
        return {idx: (sublist[0], sublist[1]) for idx, sublist in enumerate(self._marks)}
    
    def show(self):
        """
        Show the current time
        """
        print(f"Current time: {(self._current_time())}")

if __name__ == '__main__':
    pass