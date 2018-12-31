import queue
import requests
import threading
import time

from shodan import Shodan

from dork.config.config import load_configs, get_configs, get_handlers, get_api_key

QUERY_PAYLOAD = "hostname:{} {}"

class RequestEngine(object):
    def __init__(self, num_threads, api_key):
        self.num_threads = num_threads
        self.back_queue = queue.Queue()
        self.front_queue = queue.Queue()
        self.total_queued = 0

        self.api_key = api_key

        self.workers = []

        for _ in range(self.num_threads):
            t = threading.Thread(target=self.process_input, args=(Shodan(self.api_key),))
            t.start()
            self.workers.append(t)

    def queue_input(self, value):
        self.total_queued += 1
        self.back_queue.put(value)

    def dequeue_output(self):
        return self.front_queue.get()

    def process_input(self, shodan):
        while True:
            name, query = self.back_queue.get()
            if not query:
                return
            result = None
            try:
                result = shodan.search(query)
            except:
                print("API Issues, Sleeping...")
                time.sleep(1)
                self.back_queue.put((name, query))
            else:
                self.front_queue.put((name, result))



    def cleanup(self):
        for thread in self.workers:
            self.back_queue.put((None, None))

class DorkEngine(object):
    def __init__(self, target, wordlist=None):
        self.request_engine = RequestEngine(1, get_api_key())
        self.target = target
        self.config_payloads = load_configs()
        self.handlers = get_handlers()
        self._dork_target()

    def _dork_target(self):
        total_enqueued = 0
        for config in get_configs():
            payloads = self.config_payloads[config]
            for payload in payloads:
                self.request_engine.queue_input((config + '/' + payload['Name'], QUERY_PAYLOAD.format(self.target, payload['Query'])))
                total_enqueued += 1

        for _ in range(total_enqueued):
            self.process_output(self.request_engine.dequeue_output())
        self.request_engine.cleanup()

    def process_output(self, args):
        name, output = args
        if output['total'] != 0:
            type = name.split('/')[0]
            print("Results for: {}".format(name))
            self.handlers[type](output)
        else:
            print("Nothing found for: {}".format(name))
