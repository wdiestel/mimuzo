#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import liblo

sonic_path = "/home/wolfram/work/sonic-pi"
sonic_server_cmd = "app/server/bin/sonic-pi-server.rb"

guid = "mimuzo"

def sonic_jack_in():
    if not(unix_get_process("sonic-pi-server")):
        cmd = sonic_path+"/"+sonic_server_cmd
        print("Lanĉas Sonic-Pi-servon...")
        os.system(cmd)
    sonic_connect()
    print("Preta!")


def sonic_connect():
   
    # sonic_messages_buffer_init()
    try:
        server = liblo.ServerThread(4558)
        server.add_method(None,None,sonic_callback)
    except ServerError, err:
        print str(err)
        sys.exit()

    server.start()
    print "Servo lanĉita"
    sonic_osc_connect()
    print "Konektita!"
  
#@make_method(None, None)
def sonic_callback(self, path, args):
    print "received unknown message '%s'" % path

#def sonic_callback(path,args,types,src):
#   print path+" - "+args


def sonic_osc_connect():
    #client = sonic_make_osc_client("localhost",4557)
    #client = udp_client.UDPClient("localhost",4557)
    sonic_ping()
    #server = sonic_make_osc_server("localhost",4558)
    
#            (sonic-pi-osc-make-server "localhost" 4558
#                                   (lambda (path &rest args) (sonic-pi-log-message path args))))))

def sonic_ping():
    #liblo.send(("localhost",4557),"/ping",("hi"))
    sonic_send_code("play 50")

#"""
#with_fx :reverb, mix: 0.5 do
#  live_loop :oceans do
#    s = synth [:bnoise, :cnoise, :gnoise].choose, amp: rrand(0.5, 1.5), attack: rrand(0, 4), sustain: rrand(0, 2), release: rrand(1, 5#), cutoff_slide: rrand(0, 5), cutoff: rrand(60, 100), pan: rrand(-1, 1), pan_slide: rrand(1, 5), amp: rrand(0.5, 1)
#    control s, pan: rrand(-1, 1), cutoff: rrand(60, 110)
#    sleep rrand(2, 4)
#  end
#end
#""")

def sonic_send_command_with_arg(cmd,arg):
    liblo.send(("localhost",4557),"/"+cmd,guid,arg)


def sonic_send_command(cmd):
    liblo.send(("localhost",4557),"/"+cmd,guid)

def sonic_send_code(code):
    sonic_send_command_with_arg("run-code",code)


def win_get_process(process):
    tasklistrl = os.popen("tasklist").readlines()
    tasklistr = os.popen("tasklist").read()

    print(tasklistr)

    for examine in tasklistrl:
        if process == examine[0:len(process)]:
            return True
        
    return False

def unix_get_process(process):
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
    sonic_jack_in()

# voku 'main'
if __name__ == '__main__': main()
