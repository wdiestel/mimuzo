from observ import *

class Transmitter(object):
    def __init__(self,observable,instrument):
        self.observable = observable # normale "field"
        self.instrument = instrument
        observable.subscribe(self.transmit)
        
    def transmit(self,event):
        if event.name == "discharge":
            self.instrument.play(event.row,event.col,event.impuls)
        elif event.name == "update":
            self.instrument.modify(event.row,event.col,event.value)
