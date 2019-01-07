import shelve
import os

class Persistence(object):
    def __init__(self):
        self.store = shelve.open(os.path.join(os.getcwd(), 'output.shelf'))

    def contains(self, query):
        return (query in self.store)

    def put_new(self, query, value):
        self.store[query] = value

    def cleanup(self):
        self.store.close()
