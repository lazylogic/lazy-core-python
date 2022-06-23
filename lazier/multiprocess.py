from multiprocessing import Queue, Manager


class Queueable:
    queue: Queue

    def __init__(self, queue: Queue = None):
        self.queue = queue or Manager().Queue()
        super().__init__()

    def mediate(self, obj):
        raise NotImplementedError
