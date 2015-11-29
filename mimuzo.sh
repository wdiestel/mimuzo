#!/bin/bash
### BEGIN INIT INFO
# Provides: mimuzo
# Required-Start:
# Required-Stop:
# Default-Start:	2 3 4 5
# Default-Stop:		0 1 6
# Short-Description: Starts & Stops mimuzo
# Description:	Start & Stops mimuzo
### END INIT INFO

# Switch case for first param
case "$1" in
    start)
        echo "Lanchas mimuzon"

        dbus-launch /home/pi/mimuzo/start-server.sh 2>&1 > mimuzo-start.log & 
        sleep 10 ; python /home/pi/mimuzo/mimuzo-senfenestra.py  2>&1 > mimuzo-python.log &
        ;;

    stop)
        echo "Haltigas mimuzon"

        killall python
        killall ruby
        ;;

    restart)    
       echo "Relanchase mimuzon"
       ;;
    *)
       echo "(start|stop)"
      ;;
esac

exit 0

