from instrument import Instrument

class SynthCtl2(Instrument):
    def __init__(self,synth1,synth2,rows,cols):
        Instrument.__init__(self,rows,cols)
        #self.synth = synth
       
        for r in range(0,rows):
            for c in range(0,cols):
                synth_var ="$s_" + str(r) + "_" + str(c)
                pitch = 75 - 7*r + 4*c
                self.send_code("use_synth :{0}\n {1} = play {2}, sustain: 10600, release: 10600, amp: 0".format(synth1,synth_var,pitch))
        
                cmd_str = "control {1}".format(pitch,synth_var)
                self.def_mod(r,c,cmd_str+", amp: {0}")

                cmd_str2 = "use_synth :{0}\n play {1}, release: 4, amp: 1.0".format(synth2,pitch)
                self.def_key(r,c,cmd_str2)

        
