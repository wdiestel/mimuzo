#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import liblo

sonic_path = "/home/wolfram/work/sonic-pi"
sonic_server_cmd = "app/server/bin/sonic-pi-server.rb"

guid = "mimuzo"
pi_host = "localhost"
pi_port = 4557

# lanchu jackd antaue:
# jackd -R -d alsa -d hw:1

class Sonic(object):
    def jack_in(self):
        if not(self.unix_get_process("sonic-pi-server")):
            cmd = sonic_path+"/"+sonic_server_cmd
            print("Lanĉas Sonic-Pi-servon...")
            os.system(cmd)
            print("Preta!")

    def ping(self):
        send_code("play 50")

    def send_command_with_arg(self,cmd,arg):
        print "send to "+str(pi_port)+": "+cmd+" "+guid+", "+arg+"..."
        liblo.send((pi_host,pi_port),"/"+cmd,guid,arg)

    def send_command(self,cmd):
        print "send to "+str(pi_port)+": "+cmd
        liblo.send((pi_host,pi_port),"/"+cmd,guid)

    def send_code(self,code):
        self.send_command_with_arg("run-code",code)

    def win_get_process(self,process):
        tasklistrl = os.popen("tasklist").readlines()
        tasklistr = os.popen("tasklist").read()
        print(tasklistr)
        for examine in tasklistrl:
            if process == examine[0:len(process)]:
                return True
        return False

    def unix_get_process(self,process):
        for dirname in os.listdir('/proc'):
            if dirname == 'curproc':
                continue

            try:
                with open('/proc/{}/cmdline'.format(dirname), mode='rb') as fd:
                    content = fd.read().decode().split('\x00')
            except Exception:
                continue

            if process in content[0]:
                # dirname is also the number of PID
                print('{0:<12} : {1}'.format(dirname, ' '.join(content)))
                return True

        return False

def main():
    s = Sonic()
    s.jack_in()

# voku 'main'
if __name__ == '__main__': main()
