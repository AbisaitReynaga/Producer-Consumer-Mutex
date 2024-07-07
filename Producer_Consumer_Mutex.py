from multiprocessing import Process, Lock, Value
from time import sleep
from colorama import Fore, Style


class Storage():
    def __init__(self,capacity,items):
        self._capacity = Value('i', capacity)
        self._items = Value('i', items)

    @property
    def items(self):
        return self._items.value
    @items.setter
    def items(self, value):
        self._items.value = value
        
    @property
    def capacity(self):
        return self._capacity.value
        

class Producer(Process):

    def __init__(self, storage, lock):
        super().__init__()
        self._storage = storage
        self._lock = lock
    
    def produceItem(self):
        
        while self._storage.items < self._storage.capacity:
            try:
                self._lock.acquire()
                if self._storage.items < self._storage.capacity:
                    self._storage.items += 1
                    print(Fore.GREEN + f'Producing item... {Fore.WHITE}{self._storage.items}/{Fore.WHITE}{self._storage.capacity}')
                    sleep(.7)
                else:
                    print(Fore.YELLOW+'Storage is full')
            except:
                print(Fore.RED+'Error producing item')
            finally:
                self._lock.release()
                
    def run(self):
        while True:
            self.produceItem()
    
                
class Consumer(Process):
    def __init__(self,storage,lock):
        super().__init__()
        self._storage = storage
        self._lock = lock
    
    def consumeItem(self):
        while self._storage.items > 0:
            try:
                self._lock.acquire()
                if self._storage.items > 0:
                    self._storage.items -= 1
                    print(Fore.CYAN+f'Consuming item...{Fore.WHITE}{self._storage.items}/{Fore.WHITE}{self._storage.capacity}')
                    sleep(.2)
                else:
                    print(Fore.YELLOW+'Storage is empty')
            except:
                print(Fore.RED+'Error consuming item')
            finally:
                self._lock.release()
    
    def run(self):
        while True:
            self.consumeItem()
    

if __name__ == '__main__':
    
    storage = Storage(10,0)
    mutex = Lock()
    producer = Producer(storage, mutex)
    consumer = Consumer(storage, mutex)
    consumer1 = Consumer(storage, mutex)

    producer.start()
    consumer.start()
    consumer1.start()