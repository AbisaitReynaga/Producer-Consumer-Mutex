from multiprocessing import Process, Condition, Value
from time import sleep
from colorama import Fore, Style

# Storage class to store the items and capacity
class Storage():
    def __init__(self, capacity, items):
        self._capacity = Value('i', capacity)
        self._items = Value('i', items)

    # Getters and Setters
    @property
    def items(self):
        return self._items.value

    @items.setter
    def items(self, value):
        self._items.value = value

    @property
    def capacity(self):
        return self._capacity.value

# Producer class to produce the items
class Producer(Process):
    def __init__(self, storage, condition, speed=1):
        super().__init__()
        self._storage = storage
        self._condition = condition
        self._speed = speed

    # Method to produce the items
    def produceItem(self):
        with self._condition: #The handler 'with' automatically do acquire and release without using acquire and release methods
            while self._storage.items >= self._storage.capacity: #This condition check if the storage is full to produce the items
                print(Fore.YELLOW + f'Storage is full')
                self._condition.wait() # If the condition is True, the Thread will wait.
            self._storage.items += 1 #If the storage has capacity , it produce the item
            print(Fore.MAGENTA + f'{self.name}' + Fore.GREEN + f' Producing item... {Fore.WHITE}{self._storage.items}/{Fore.WHITE}{self._storage.capacity}')
            self._condition.notify_all() #If have been add one item to storage, It will be notify all threads waiting.
        sleep(self._speed)  # Sleep for the speed

    # Run method to start the process
    def run(self):
        while True:
            self.produceItem()

# Consumer class to consume the items
class Consumer(Process):
    def __init__(self, storage, condition, speed=2):
        super().__init__()
        self._storage = storage
        self._condition = condition
        self._speed = speed

    # Method to consume the items
    def consumeItem(self):
        with self._condition: #The handler 'with' automatically do acquire and release without using acquire and release methods
            while self._storage.items <= 0: #This condition check if the storage isn't empty to consume a item.
                print(Fore.YELLOW + f'Storage is empty')
                self._condition.wait() # If the condition is True, the Thread will wait.
            self._storage.items -= 1 #If the storage has items , it consume the item
            print(Fore.MAGENTA + f'{self.name}' + Fore.GREEN + f' Consuming item... {Fore.WHITE}{self._storage.items}/{Fore.WHITE}{self._storage.capacity}')
            self._condition.notify_all()  #If have been consume one item to storage, It will be notify all threads 
        sleep(self._speed)  # Sleep for the speed

    # Run method to start the process
    def run(self):
        while True:
            self.consumeItem()

# Main method to start the program
if __name__ == '__main__':
    print(Fore.RESET)
    capacity = int(input('Enter the storage capacity: '))  # Get the storage capacity
    qtyProducer = int(input('Enter the number of producers: '))  # Get the number of producers
    qtyConsumer = int(input('Enter the number of consumers: '))  # Get the number of consumers

    storage = Storage(capacity, 0)  # Create the storage object
    condition = Condition()  # Create the condition object

    producers = [Producer(storage, condition) for _ in range(qtyProducer)]  # Create the producers
    consumers = [Consumer(storage, condition) for _ in range(qtyConsumer)]  # Create the consumers

    for consumer in consumers:
        consumer.start()

    for producer in producers:
        producer.start()

    for consumer in consumers:
        consumer.join()

    for producer in producers:
        producer.join()
