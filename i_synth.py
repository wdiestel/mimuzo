from instrument import Instrument

class Synth(Instrument):
    def __init__(self,synth,rows,cols,release=1):
        Instrument.__init__(self,rows,cols)
        self.synth = synth
        for r in range(0,rows):
            for c in range(0,cols):
                pitch = 90 - 7*r + 4*c
                str = "use_synth :{0}\n play {1}, release: {2}".format(synth,pitch,release)
                self.def_key(r,c,str)
        
        
