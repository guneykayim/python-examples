from multiprocessing import Process, Queue, Lock, Manager
from multiprocessing.managers import BaseManager
import time
import logging
import random

logging.basicConfig(level=logging.DEBUG, format='(%(processName)-9s) %(message)s',)
NUMBER_OF_PROCESSES = 8

class SimpleDataType():
    """
    a simple class which should be regitered using multiprocessing.BaseManager 
    because we want this class to be shared accross multiple processes
    """

    def __init__(self):
        self.data = list()
    
    def addData(self, d):
        self.data.append(d)

    def printData(self):
        logging.debug(f'data: {self.data}')

class SampleProcess(Process):
    def __init__(self, shared_data, lock, queue=None, id=None, kwargs=None):
        super().__init__()
        self.kwargs = kwargs
        self.queue = queue
        self.id = id
        self.data = shared_data
        self.lock = lock
        return

    def run(self):
        """
        wait random amount of time and append id to shared data
        there should be a lock protection as multiple different processes can try to access the shared data at the same time
        """

        logging.debug(f'Running process id={self.id}')
        r = random.uniform(0, 5)
        time.sleep(r)
        self.lock.acquire()
        self.data.addData(self.id)
        self.lock.release()
        self.queue.put(f'Process id={self.id} finished running in {r} seconds')

if __name__ == '__main__':
    # register the SimpleDataType class so that we can create an instance of it using a multiprocessing.BaseManager
    # later on, an instance of SimpleDataType class can be shared across multiple processes
    BaseManager.register('SimpleDataType', SimpleDataType)
    manager = BaseManager()
    manager.start()

    # create an instance of SimpleDataType class using multiprocessing.BaseManager
    shared_data = manager.SimpleDataType()

    logging.debug('Starting processes')

    # create a list to hold running SampleProcess object instances
    processes = list()

    # build a single queue to send to all process objects
    q = Queue()  

    # build a single lock to send to all process objects
    lock = Lock()

    for i in range(NUMBER_OF_PROCESSES):
        p = SampleProcess(shared_data, lock, queue=q, id=i)
        p.start()
        processes.append(p)

    # wait until all processes are finished
    logging.debug('waiting for all processes to finish running')
    [proc.join() for proc in processes]

    logging.debug('all processes are finished running')

    # we'll see that shared_data is populated with random access from processes based on how long it took them to process
    shared_data.printData()
    
    logging.debug('results')
    while not q.empty():
        logging.debug(q.get())
