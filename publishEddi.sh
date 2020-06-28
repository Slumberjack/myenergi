#! /bin/bash

source /home/rwj/bin/dev_env

cd /home/rwj/python/myenergi
while true
 do
 nohup ./eddi.py >> $LOGDIR/publishEddi.log 
done
