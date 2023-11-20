import time
#import socket
import signal, sys

import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

#import adafruit_tsl2561
#sensor = adafruit_tsl2561.TSL2561(i2c)
import adafruit_tsl2591
sensor = adafruit_tsl2591.TSL2591(i2c)


#MQQTT Cliente Raspberry SkyGlow Monitor

import paho.mqtt.client as mqtt

hostname = "mqtt.eclipseprojects.io"
broker_port = 1883
topic = "el_topico/rpi2"

client = mqtt.Client()

client.connect(hostname, broker_port, 60)

#client.loop_start()
#client.loop_stop()

#def send_mqtt(message):



#ads = ADS.ADS1115(i2c, 1, None, 256, 0x49)
ads = ADS.ADS1115(i2c, 2/3)

chan_0 = AnalogIn(ads, ADS.P0)
chan_1 = AnalogIn(ads, ADS.P1)
chan_2 = AnalogIn(ads, ADS.P2)
chan_3 = AnalogIn(ads, ADS.P3)

tiempo_inicio = time.strftime("%Y%m%dT%H%M%S")

baconFile = open(f'{tiempo_inicio}_SKYGLOW_LABSENS.txt', 'w') #crea el archivo
baconFile.write('tiempo (unix-time), canal 1 (counts), canal 2 (counts), canal 3 (counts), canal 4 (counts), tsl (lux)\n') #escribe un encabezado
baconFile.close()

def signal_handler(signal, frame):
    print('\nkill command received from keyboard - script exiting')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
    try:
        timestamp = time.time()
        valor_chan_0 = chan_0.value
        valor_chan_1 = chan_1.value
        valor_chan_2 = chan_2.value
        valor_chan_3 = chan_3.value
        #valor_tsl = sensor.lux
        valor_lux = sensor.lux
        
        print(chan_0.value, chan_0.voltage, chan_1.value, chan_1.voltage, chan_2.value, chan_2.voltage, chan_3.value, chan_3.voltage)
        #print(chan_0.value, chan_0.voltage)
        #print('Lux: {}'.format(sensor.lux))
        print("Total light: {} [lux]".format(sensor.lux))
    
        client.publish(topic, valor_chan_0) #mqqt_send
    
        baconFile = open(f'{tiempo_inicio}_SKYGLOW_LABSENS.txt', 'a') #abre el archivo
        baconFile.write(f'{timestamp}\t{valor_chan_0}\t{valor_chan_1}\t{valor_chan_2}\t{valor_chan_3}\t{valor_lux}\n') #escribe la data y la estampa de tiempo
        baconFile.close()
    
        time.sleep(10)
    
    except:
        client.disconnect()
        print('desconectando mqtt...')
        
        break
    
print('#####finalizó el proceso#####')
