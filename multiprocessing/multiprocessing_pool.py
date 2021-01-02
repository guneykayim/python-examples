from multiprocessing import Process, Pool
import multiprocessing
import time
import logging
import random

logging.basicConfig(level=logging.DEBUG, format='(%(processName)-9s) %(message)s',)
POOL_SIZE = 4
NUMBER_OF_PROCESSES = 10

class SampleObject():
    def __init__(self, id=None, kwargs=None):
        self.id = id
        self.kwargs = kwargs
        return

def run(obj):
    """
    A dummy function which takes an object and does some processing.
    In this examples, it just waits random amount of time and returns a sample string.
    """
    logging.debug(f'Running process id={obj.id}')
    r = random.uniform(0, 5)
    time.sleep(r)
    return (f'Process id={obj.id} took {r} seconds to run')

if __name__ == '__main__':
    
    logging.debug(f'Number of cpu: {multiprocessing.cpu_count()}')
    logging.debug(f'Pool size: {POOL_SIZE}')
    logging.debug(f'Number of processes: {NUMBER_OF_PROCESSES}')

    objs = []
    for i in range(NUMBER_OF_PROCESSES):
        objs.append(SampleObject(id=i))
    
    logging.debug('Starting processes')
    with Pool(processes = POOL_SIZE) as pool:
        res = pool.map(run, objs)
    
    logging.debug('All processes are finished running')
    logging.debug('Results:')
    for r in res:
        logging.debug(r)
