from instrument import Instrument

class SynthCtl(Instrument):
    def __init__(self,synth,rows,cols):
        Instrument.__init__(self,rows,cols)
        self.synth = synth
       
        for r in range(0,rows):
            for c in range(0,cols):
                synth_var ="$s_" + str(r) + "_" + str(c)
                pitch = 40 - 7*r + 4*c
                self.send_code("use_synth :{0}\n {1} = play {2}, release: 50, amp: 0".format(synth,synth_var,pitch))
        
                cmd_str = "control {1}".format(pitch,synth_var)
                self.def_key(r,c,cmd_str+", amp: {0}")
                self.def_mod(r,c,cmd_str+", amp: {0}")
        
