from instrument import Instrument

class SynthCtl(Instrument):
    def __init__(self,synth,rows,cols):
        Instrument.__init__(self,rows,cols)
        self.synth = synth
        self.send_code("use_synth :{0}\n $s = play 60, release: 50".format(synth))
        
        for r in range(0,rows):
            for c in range(0,cols):
                pitch = 90 - 7*r + 4*c
                str = "control $s, note: {0}".format(pitch)
                self.def_key(r,c,str+", amp: {0}")
        
