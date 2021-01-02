import threading, queue
import time
import random
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)
NUMBER_OF_THREADS = 4
TIMEOUT_SECONDS = 5

class SampleThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, id=None, kwargs=None):
        super().__init__(group=group, target=target, name=name)
        self.id = id
        self.kwargs = kwargs
        self.queue = kwargs['queue']
        self.trigger = kwargs['trigger']
        self.response = kwargs['response']
        self.timeout_seconds = kwargs['timeout']
        return

    def run(self):
        while True:
            if not self.trigger.isSet():
                logging.debug('Waiting for trigger')
                self.response.clear()
                event_is_set = self.trigger.wait(self.timeout_seconds)
                if(event_is_set):
                    r = random.uniform(0, 5)
                    time.sleep(r)
                    self.queue.put(f'Thread id={self.id} finished running in {r} seconds')
                    self.response.set()
                else:
                    logging.debug('Wait timed out')
                    break

if __name__ == '__main__':

    print('Starting threads')
    # build a single queue to send to all thread objects
    q = queue.Queue() 
    # build a single trigger to send to all thread objects (we want all of them to run at the same time)
    trigger = threading.Event()
    # create a list to hold responses from all thread objects
    responses = list()

    for i in range(NUMBER_OF_THREADS):
        r = threading.Event()
        responses.append(r)
        t = SampleThread(id = i, kwargs={'queue':q, 'trigger':trigger, 'response': r, 'timeout':TIMEOUT_SECONDS})
        t.start()

    i = 0
    while True:
        logging.debug('Waiting before triggering event')
        time.sleep(random.uniform(1, 3))
        trigger.set()
        logging.debug('Event triggered %d, now waiting for threads to finish and respond', i)
        i+=1

        for r in responses:
            while not r.isSet():
                r.wait()
        
        logging.debug('All threads are responded')
        logging.debug('Results')
        while not q.empty():
            logging.debug(q.get())

        trigger.clear()
        if(i >= 3):
            logging.debug('No more triggers will be sent')
            break