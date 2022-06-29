# new adafruit package
# sudo pip install adafruit-circuitpython-dht 
# sudo apt install libgpiod2

import adafruit_dht as dht
import board
import time

SENSOR = dht.DHT11(board.D4) #gpio 기준 4번
while True:
    try: 
        t = SENSOR.temperature
        h = SENSOR.humidity
        print(f'TEMP > {t: .1f}`C // HUMID > {h:.1f}%')

    except RuntimeError  as e:
        print(f'ERROR > {e.args[0]}')
        time.sleep(3.0)
    except Exception as e:
        SENSOR.exit()
        raise e #발생한 오류를 다른 곳에 보낸다. 

    time.sleep(3.0)


