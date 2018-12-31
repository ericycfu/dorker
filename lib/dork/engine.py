import queue
import requests
import threading

from shodan import Shodan

from dork.config.config import load_configs, get_configs

API_KEY = ""

QUERY_PAYLOAD = "hostname:{} {}"

class RequestEngine(object):
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.back_queue = queue.Queue()
        self.front_queue = queue.Queue()
        self.total_queued = 0

        self.workers = []

        for _ in range(self.num_threads):
            t = threading.Thread(target=self.process_input, args=(Shodan(API_KEY),))
            t.start()
            self.workers.append(t)

    def queue_input(self, value):
        self.total_queued += 1
        self.back_queue.put(value)

    def dequeue_output(self):
        return self.front_queue.get()

    def process_input(self, shodan):
        while True:
            query = self.back_queue.get()
            if not query:
                return
            result = shodan.search(query)
            self.front_queue.put(result)



    def cleanup(self):
        for thread in self.workers:
            self.back_queue.put(None)

class DorkEngine(object):
    def __init__(self, target, wordlist=None):
        self.request_engine = RequestEngine(1)
        self.target = target
        self.config_payloads = load_configs()
        self._dork_target()

    def _dork_target(self):
        total_enqueued = 0
        for config in get_configs():
            payloads = self.config_payloads[config]
            for payload in payloads:
                self.request_engine.queue_input(QUERY_PAYLOAD.format(self.target, payload['Query']))
                total_enqueued += 1

        for _ in range(total_enqueued):
            print(self.request_engine.dequeue_output())
        self.request_engine.cleanup()
