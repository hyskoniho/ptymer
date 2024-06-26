from datetime import datetime, timedelta
from time import sleep

class Timer:
    def __init__(self):
        self.__start_time: datetime | None = None
        self._marks: list = []
        self.__running: bool = False
    
    @staticmethod
    def time_format(secs: int | float) -> datetime.time:
        mins, secs = divmod(secs, 60)
        horas, mins = divmod(mins, 60)

        time_str = f"{int(horas)} {int(mins)} {secs}"
        return datetime.strptime(time_str, "%H %M %S.%f").time()
        
    def start(self, seconds: int | float | None = None) -> None:
        """
        
        """
        self.__running = True
        self.__start_time = datetime.now()
        self.__end_time = self.__start_time + timedelta(seconds=seconds) if seconds else None
    
    def stop(self, show: bool = False) -> datetime.time:
        """
        Para o timer e pode retornar o tempo restante no seguinte 
        formato: HH:MM:SS.ms
        """
        if not self.__running:
            raise AttributeError(f"Não há timer em execução!")

        self.__running = False
        self.__end_time = self.time_format((datetime.now() - self.__start_time).total_seconds())

        print(f"Endpoint: {self.__end_time}") if show else None
        [print(f"Mark {x+1}: {mark[0]}{" \t " if mark[1] else ""}'{mark[1]}'") for x, mark in enumerate(self._marks)] if show and len(self._marks) > 0 else None
        return self.__end_time
    
    def show(self) -> str:
        """
        Exibe o tempo restante do timer no formato HH:MM:SS.ms
        """
        if not self.__running:
            raise AttributeError(f"Não há timer em execução!")
        
        return str(self.time_format((datetime.now() - self.__start_time).total_seconds()))
    
    def mark(self, observ: None | str = None) -> None:
        """
        Marca o tempo atual do timer
        """
        self._marks.append([self.show(), observ if observ else ""])

if __name__ == '__main__':
    timer = Timer()
    timer.start()
    
    sleep(3)

    timer.mark("Primeiro marco")
    sleep(0.1)
    timer.mark()
    sleep(0.1)
    timer.mark(" Segundo marco")
    sleep(0.1)
    timer.mark()
    sleep(0.1)

    sleep(3)
    timer.mark("     Terceiro marco")
    sleep(5)
    timer.mark()
    sleep(1)

    timer.stop(True)