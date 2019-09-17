#!/bin/bash

LOGFILE="/home/pi/weather_i2c/log.txt"
TIMESTAMP=`date "+%Y-%m-%d %H:%M:%S"`

echo execute.sh inicializado.
sleep 20s
echo Registrando - log.txt
echo Executando - weather-com.py
echo $TIMESTAMP weather_inicializado >> $LOGFILE
sleep 2s

python3 /home/pi/weather_i2c/weather-com.py
