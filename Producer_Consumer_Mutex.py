from multiprocessing import Process, Lock, Value
from time import sleep
from colorama import Fore, Style

#Storage class to store the items and capacity
class Storage():
    def __init__(self,capacity,items):
        self._capacity = Value('i', capacity)
        self._items = Value('i', items)

    #Getters and Setters
    @property
    def items(self):
        return self._items.value
    @items.setter
    def items(self, value):
        self._items.value = value
        
    @property
    def capacity(self):
        return self._capacity.value
        

#Producer class to produce the items
class Producer(Process):

    def __init__(self, storage, lock,speed=0.5):
        super().__init__()
        self._storage = storage
        self._lock = lock
        self._speed = speed

    #Method to produce the items
    def produceItem(self):
        
        while self._storage.items < self._storage.capacity: #Check if the storage is empty to produce the items
            try:
                self._lock.acquire() #Acquire the lock
                if self._storage.items < self._storage.capacity: #Check if the storage is empty to produce the items
                    self._storage.items += 1 #If the storage is empty, produce the item
                    print(Fore.MAGENTA+f'{self.name}'+Fore.GREEN + f' Producing item... {Fore.WHITE}{self._storage.items}/{Fore.WHITE}{self._storage.capacity}')
                    sleep(self._speed)#Sleep for the speed
                else:
                    print(Fore.YELLOW+f'Storage is full')
                    sleep(self._speed)
            except:
                print(Fore.RED+'Error producing item')
            finally:
                self._lock.release() #Release the lock
        print(Fore.YELLOW+'Storage is full')
        sleep(self._speed)
    #Run method to start the process  
    def run(self):
        self.produceItem()

#Consumer class to consume the items
class Consumer(Process):
    def __init__(self,storage,lock,speed=0.2):
        super().__init__()
        self._storage = storage
        self._lock = lock
        self._speed = speed
    #Method to consume the items
    def consumeItem(self):
        while self._storage.items > 0: #Check if the storage have items to consume
            try:
                self._lock.acquire() #Acquire the lock
                if self._storage.items > 0:  #Check if the storage have items to consume
                    self._storage.items -= 1 #If the storage have items, consume the item
                    print(Fore.CYAN+f'{self.name}'+Fore.CYAN+f' Consuming item...{Fore.WHITE}{self._storage.items}/{Fore.WHITE}{self._storage.capacity}')
                    sleep(self._speed)#Sleep for the speed
                else:
                    print(Fore.YELLOW+f'Storage is empty')
                    sleep(self._speed )

            except:
                print(Fore.RED+'Error consuming item')
            finally:
                self._lock.release()
        print(Fore.YELLOW+'Storage is empty')
        sleep(self._speed)
    #Run method to start the process
    def run(self):
        self.consumeItem()

#Main method to start the program
if __name__ == '__main__':
    
    print(Fore.RESET)
    capacity = int(input('Enter the storage capacity: ')) #Get the storage capacity
    qtyProducer = int(input('Enter the number of producers: ')) #Get the number of producers
    qtyConsumer = int(input('Enter the number of consumers: ')) #Get the number of consumers
    
    storage = Storage(capacity,0) #Create the storage object
    mutex = Lock() #Create the mutex object
    
    producers = [Producer(storage,mutex) for i in range(qtyProducer)]#Create the producers
    consumers = [Consumer(storage,mutex) for i in range(qtyConsumer)]#Create the consumers
    
    
    #Start the producers and consumers
    for producer in producers:
        producer.start()
        
    #Start the consumers
    for consumer in consumers:
        consumer.start()
        
    #Join the producers and consumers
    for consumer in consumers:
        consumer.join()
    for consumer in consumers:
        consumer.join()
