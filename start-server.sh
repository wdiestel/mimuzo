#!/bin/bash

# ne malrapidigu la kameraon pro malheleco
/usr/bin/v4l2-ctl -c exposure_auto_priority=0

/usr/bin/jackd -R -T -p 32 -d alsa -d hw:1 -n 3 -p 2048 -r 44100 &

wait 3

###/usr/bin/scsynth -u 4556 -m 131072 -a 64 -z 256 -U /usr/lib/SuperCollider/plugins:/opt/sonic-pi/app/server/native/raspberry/extra-ugens/

/usr/bin/ruby ~/work/sonic-pi/app/server/bin/sonic-pi-server.rb &

