import threading
import time
import random

class ThreadFactory(object):
    """@Brief: Prodcuer-Consumer Factory"""
    queue = []
    lock = threading.Lock()
    condition = threading.Condition()

    class Producer(threading.Thread):
        def run(self):
            nums = range(5)
            while True:
                ThreadFactory.condition.acquire()
                num = random.choice(nums)
                ThreadFactory.queue.append(num)
                print "Produce %d" % num
                ThreadFactory.condition.notify()
                ThreadFactory.condition.release()
                time.sleep(random.random())
            
    class Consumer(threading.Thread):
        def run(self):
            while True:
                ThreadFactory.condition.acquire()
                if not ThreadFactory.queue:
                    print "Nothing in queue, consumer is waiting"
                    ThreadFactory.condition.wait()
                    print "producer added sth. to queue and nodified the consumer"
                num = ThreadFactory.queue.pop(0)
                print "Consume %d" % num
                ThreadFactory.condition.release()
                time.sleep(random.random())

if __name__  == '__main__':
    a = ThreadFactory.Producer()
    b = ThreadFactory.Consumer()
    a.start()
    b.start()

