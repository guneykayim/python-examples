from multiprocessing import Process, Queue
import time
import logging
import random

logging.basicConfig(level=logging.DEBUG, format='(%(processName)-9s) %(message)s',)
NUMBER_OF_PROCESSES = 8

class SampleProcess(Process):
    def __init__(self, queue=None, id=None, kwargs=None):
        super().__init__()
        self.kwargs = kwargs
        self.queue = queue
        self.id = id
        return

    def run(self):
        # do some work here
        logging.debug(f'Running process id={self.id}')
        r = random.uniform(0, 5)
        time.sleep(r)
        self.queue.put(f'Process id={self.id} finished running in {r} seconds')

if __name__ == '__main__':
    
    logging.debug('Starting processes')
    # Create a list to hold running SampleProcess object instances...
    processes = list()
    # Build a single queue to send to all process objects...
    q = Queue()  
    for i in range(NUMBER_OF_PROCESSES):
        p = SampleProcess(queue=q, id=i)
        p.start()
        processes.append(p)

    # wait until all processes are finished
    logging.debug('Waiting for all processes to finish running')
    [proc.join() for proc in processes]

    logging.debug('All processes are finished running')
    logging.debug('Results')
    while not q.empty():
        logging.debug(q.get())
