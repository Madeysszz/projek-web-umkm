# adts/stack_adt.py
from utils.exceptions import EmptyStackException

class StackAbsen:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        raise EmptyStackException("Stack kosong.")

    def is_empty(self):
        return len(self.stack) == 0

    def lihat_stack(self):
        return self.stack.copy()