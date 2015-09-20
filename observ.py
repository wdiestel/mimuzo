class Event(object):
    pass

class Observable(object):
    def __init__(self):
        self.callbacks = []
    def subscribe(self, callback):
        self.callbacks.append(callback)
    def fire(self, event):
        # fn(event)
        #e = Event()
        #e.source = self
        #for k, v in attrs.iteritems():
        #    setattr(e, k, v)
        for fn in self.callbacks:
            fn(event)
