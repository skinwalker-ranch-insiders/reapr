#!/bin/sh
while true
do
   pgrep -f 'python3 ./reapr'>/dev/null
   if [[ $? -ne 0 ]] ; then
        echo "Restarting REAPR:     $(date)" >> ./reapr_restarts.txt
        /usr/local/bin/python3 ./reapr.py
   fi
done
