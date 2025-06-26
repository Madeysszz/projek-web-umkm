# adts/queue_adt.py
from collections import deque
from utils.exceptions import EmptyQueueException

class QueueAbsen:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.popleft()
        raise EmptyQueueException("Antrian kosong.")

    def is_empty(self):
        return len(self.queue) == 0

    def lihat_queue(self):
        return list(self.queue)