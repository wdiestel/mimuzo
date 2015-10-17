#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import liblo

sonic_path = "/home/wolfram/work/sonic-pi"
sonic_server_cmd = "app/server/bin/sonic-pi-server.rb"

sonic_version = 2.6
guid = "mimuzo"
pi_host = "localhost"
pi_port = 4557

# lanchu jackd antaue:
# jackd -R -d alsa -d hw:1

class Sonic(object):
    def jack_in(self):
        pass
#        if not(self.unix_get_process("sonic-pi-server")):
#            cmd = sonic_path+"/"+sonic_server_cmd
#            print("Lanĉas Sonic-Pi-servon...")
#            os.system(cmd)
#            print("Preta!")

    def __del__(self):
        self.stop_jobs()

    def ping(self):
        send_code("play 50")

    def send_command_with_arg(self,cmd,arg):
        if sonic_version > 2.6:
            print "send to "+str(pi_port)+": "+cmd+" "+guid+", "+arg+"..."
            liblo.send((pi_host,pi_port),"/"+cmd,guid,arg)
        else:
            print "send to "+str(pi_port)+": "+cmd+", "+arg+"..."
            liblo.send((pi_host,pi_port),"/"+cmd,arg)

    def send_command(self,cmd):
        if sonic_version > 2.6:
            print "send to "+str(pi_port)+": "+cmd
            liblo.send((pi_host,pi_port),"/"+cmd,guid)
        else:
            print "send to "+str(pi_port)+": "+cmd
            liblo.send((pi_host,pi_port),"/"+cmd)

    def send_code(self,code):
        self.send_command_with_arg("run-code",code)

    def stop_jobs(self):
        self.send_command("stop-all-jobs")

def main():
    s = Sonic()
    s.jack_in()

# voku 'main'
if __name__ == '__main__': main()
