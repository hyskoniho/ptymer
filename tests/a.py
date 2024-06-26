from timer import Timer
from time import sleep

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