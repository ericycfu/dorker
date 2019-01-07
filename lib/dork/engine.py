import queue
import requests
import threading
import time

from shodan import Shodan

from dork.config.config import DorkerConfiguration
from dork.persist import Persistence

PAYLOADS = {
    'url': "hostname:{} {}",
    'org': "org:{} {}",
}

class RequestEngine(object):
    def __init__(self, api_keys):
        self.back_queue = queue.Queue()
        self.front_queue = queue.Queue()
        self.total_queued = 0

        self.workers = []

        for key in api_keys:
            t = threading.Thread(target=self.process_input, args=(Shodan(key),))
            t.start()
            self.workers.append(t)

    def queue_input(self, value):
        self.total_queued += 1
        self.back_queue.put(value)

    def dequeue_output(self):
        self.total_queued -= 1
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
                time.sleep(1)
                self.back_queue.put((name, query))
            else:
                self.front_queue.put((name, result))

    def cleanup(self):
        for thread in self.workers:
            self.back_queue.put((None, None))

class DorkEngine(object):
    def __init__(self):
        self.configuration = DorkerConfiguration()
        self.config_payloads = self.configuration.SOURCES
        self.handlers = self.configuration.HANDLERS

        self.request_engine = RequestEngine(self.configuration.API_KEYS)
        self.persistent_store = Persistence()

        self.to_notify = []

    def dork_target(self, target, payload_type, org=None):
        for config in self.configuration.CONFIGS:
            payloads = self.config_payloads[config]
            for payload in payloads:
                id = target
                if org:
                    id = org + '/' + id
                self.request_engine.queue_input((id + '/' + config + '/' + payload['Name'], PAYLOADS[payload_type].format(target, payload['Query'])))

    def dump_target(self):
        while self.request_engine.total_queued > 0:
            print(self.request_engine.total_queued)
            self.process_output(self.request_engine.dequeue_output())
        self.request_engine.cleanup()
        self.persistent_store.cleanup()

        for item in self.to_notify:
            print(item)

    def process_output(self, args):
        name, output = args
        print("Processing {}".format(name))
        if output['total'] != 0:
            type = name.split('/')[-2]
            output['path'] = name
            to_notify = self.handlers[type](output, self.persistent_store)
            self.to_notify.append(to_notify)
