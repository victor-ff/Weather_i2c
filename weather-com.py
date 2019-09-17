#!/usr/bin/python3
#-*- coding: utf-8 -*-

import I2C_LCD_driver
import pywapi
import time
import string
import subprocess

## Drive Tela_LCD
DriveLCD = I2C_LCD_driver.lcd()

## Variaveis.
vTempRasp = subprocess.getoutput("vcgencmd measure_temp | cut -c 6-9")
vTimerUpdade = 1
vTimerDiagnostic = 1
vCond = 'null'
vTempC = 'null'
bLoopWhile = True

## Teste display LCD.
print("Setting LCD.")
time.sleep(0.5)
DriveLCD.lcd_clear()
DriveLCD.lcd_display_string("Loading..", 2, 2)
DriveLCD.lcd_display_string("..Weather.com", 3, 2)
time.sleep(1)
DriveLCD.lcd_clear()

print("Loop started")
while bLoopWhile:

    ## Conecta na api Weather.com para atualizar as informações.
    vTimerUpdade -= 1
    if vTimerUpdade == 0:
        DriveLCD.lcd_clear()
        DriveLCD.lcd_display_string("Synchronizing..", 2, 2)
        time.sleep(0.5)
        print("... connecting Weather.com")
        weather = pywapi.get_weather_from_weather_com('BRXX0228')

            # BRXX0228 - SJC
            # USNV0049 - Las Vegas, Nevada

        vCond = str.lower(weather['current_conditions']['text'])
        vTempC = str(weather['current_conditions']['temperature'])
        vUltimoUpdate = str(weather['current_conditions']['last_updated'])
        vCity = str(weather['current_conditions']['station'])
        vTimerUpdade = 900

        ## Confere a variável com a condição climatica e atualiza com o texto traduzido.
        if vCond == 'cloudy':
            vCond = 'Esta nublado'
        elif vCond == 'partly cloudy':
            vCond = 'Parc.Nublado'
        elif vCond == 'mostly cloudy':
            vCond = 'Encoberto'
        elif vCond == 'fair':
            vCond = 'Tempo limpo'
        elif vCond == 'clear':
            vCond = 'Ceu claro'
        elif vCond == 'fog':
            vCond = 'Com nevoa'
        elif vCond == 'haze':
            vCond = 'Neblina'
        elif vCond == 'light rain':
            vCond = 'Chuva leve'
        elif vCond == 'rain':
            vCond = 'Chuva'
        elif vCond == 'thunder':
            vCond = 'Trovoada'
        elif vCond == 't-storm':
            vCond = 'Pancad. chuva'
        elif vCond == 'light rain with thunder':
            vCond = 'Chuva e trovao'

        ## Faz a limpeza da tela e printa os valores climaticos.
        DriveLCD.lcd_clear()
        DriveLCD.lcd_display_string(vCond, 3, 1)
        DriveLCD.lcd_display_string("{}'C".format(vTempC), 3, 15)
        ## (Print via terminal) - Captura cidade e hora do ultimo update da API.
        print("Status: {}, {}".format(vCity, vUltimoUpdate))
        print("Weather: {}, {}".format(vCond, vTempC))
        print()

    ## Monitoramento de temperatura da RaspberryPi ##
    vTimerDiagnostic -= 1
    if vTimerDiagnostic == 0:
        vTempRasp = subprocess.getoutput("vcgencmd measure_temp | cut -c 6-7")
        DriveLCD.lcd_display_string("RaspberryPi", 4, 1)
        DriveLCD.lcd_display_string("{}'C".format(vTempRasp), 4, 15)
        vTimerDiagnostic = 5

    ## Variáveis para atualização de data e hora ##
    vDataDMA = time.strftime("%d.%b.%y")
    #vDataAMD = time.strftime("%y.%b.%d")   # Decidi não utilizar, esta estranho. #
    vHoraHMS = time.strftime("%H:%M:%S")

    ## (Print via terminal) - Confirmar a funcionalidade das variaveis ##
    print("{}-{}  {} {}C {}C ({} {}) ".format(vDataDMA, vHoraHMS, vCond, vTempC, vTempRasp, vTimerUpdade, vTimerDiagnostic))

    ## Informação na Tela_LCD ##
    DriveLCD.lcd_display_string("{}".format(vDataDMA), 1, 1)
    DriveLCD.lcd_display_string("{}".format(vHoraHMS), 1, 11)
    time.sleep(1)
