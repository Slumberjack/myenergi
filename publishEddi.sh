#! /bin/bash

source /home/rwj/bin/dev_env

cd /home/rwj/python/eddi
while true
 do
 nohup ./eddi.py >> $LOGDIR/publishEddi.log 
done
