from instrument import Instrument

class Fm(Instrument):
    def __init__(self,rows,cols):
        Instrument.__init__(self,rows,cols)
        for r in range(0,rows):
            for c in range(0,cols):
                pitch = 90 - 7*r + 4*c
                self.def_key(r,c,"use_synth :fm\nplay "+str(pitch))
        
        
