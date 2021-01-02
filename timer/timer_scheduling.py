from threading import Timer
from datetime import datetime
import time
import random
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)

class ScheduledTimer():
    def __init__(self, kwargs=None):
        fps = kwargs.get('fps', 30)
        self.autoStop = kwargs.get('autostop', True)
        self.callable = kwargs.get('target', self.run)
        self.waitTime = (1000.0 / fps) / 1000.0
        self.__stop = False
        logging.debug(f'ScheduledThread initialised with wait time: {self.waitTime}')

    def run(self):
        """
        The function that runs when the timer ticks.
        """
        time.sleep(random.uniform(0, 0.05))

    def start(self):
        """
        Starts thread clock.
        """
        start_time = datetime.now()
        logging.debug(f'Ran callable at: {datetime.now().time()}')
        self.callable()
        time_diff = (datetime.now() - start_time).total_seconds()
        self.timeSpent = min(self.waitTime, time_diff)

        self.__clock = Timer(self.waitTime-self.timeSpent, self.start)
        self.__clock.daemon = self.autoStop
        self.__clock.start()
        if(self.__stop):
            self.__clock.cancel()

    def stop(self):
        """
        Stops thread clock.
        """
        self.__stop = True
        logging.debug('Stopping scheduled timer')

def bar():
    logging.debug(f'Just another function')
    time.sleep(random.uniform(0, 0.05))

if __name__ == '__main__':
    sched = ScheduledTimer(kwargs={'fps':30})
    sched.start()
    time.sleep(2)
    sched.stop()

    sched = ScheduledTimer(kwargs={'target':bar, 'fps':5})
    sched.start()
    time.sleep(2)
    sched.stop()