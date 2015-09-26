from instrument import Instrument

class Synth(Instrument):
    def __init__(self,synth,rows,cols):
        Instrument.__init__(self,rows,cols)
        self.synth = synth
        for r in range(0,rows):
            for c in range(0,cols):
                pitch = 90 - 7*r + 4*c
                self.def_key(r,c,"use_synth :"+synth+"\nplay "+str(pitch))
        
        
