import queue
import requests
import threading

class RequestEngine(object):
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.back_queue = queue.Queue()
        self.front_queue = queue.Queue()
        self.total_queued = 0

        self.workers = []

        for _ in range(self.num_threads):
            t = threading.Thread(target=self.process_input)
            t.start()
            self.workers.append(t)

    def queue_input(self, value):
        self.total_queued += 1
        self.back_queue.put(value)

    def dequeue_output(self):
        return self.front_queue.get()

    def process_input(self):
        while True:
            url = self.back_queue.get()
            if not url:
                return
            resp = requests.get(url)
            self.front_queue.put(resp.text)

    def cleanup(self):
        for thread in self.workers:
            self.back_queue.put(None)
