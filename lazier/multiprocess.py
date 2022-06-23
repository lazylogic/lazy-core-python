from multiprocessing import Queue, Manager


class Queueable:
    queue: Queue

    def __init__(self, queue: Queue = None):
        super().__init__()
        self.queue = queue or Manager().Queue()

    def mediate(self, obj):
        raise NotImplementedError
