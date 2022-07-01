# MQTT Pub/Sub App 

from threading import Thread, Timer
import time 
import datetime as dt 
import paho.mqtt.client as mqtt
import json
import datetime as dt

import adafruit_dht as dht #DHT 센서용
import board 

#LED 
import RPi.GPIO as GPIO 

# 온습도센서가 이미 BCM 모드로 해서, GPIO 숫자를 입력해야한다. (같은 mode로 지정해줘야 함) 
RED = 17
BLUE = 27 
SENSOR = dht.DHT11(board.D4) #DHT11

# LED setup 
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)

#DHT 센서값 Publish
class publisher(Thread) : #Thread를 상속받는 클래스
    def __init__(self):
        Thread.__init__(self)
        self.host = '' #local host #추후 변경 #ip
        self.port =   #port 
        print('Publisher 스레드 시작')
        self.client = mqtt.Client(client_id = 'EMS01')
        

    def run(self):
        self.client.connect(self.host,self.port)
        self.publish_data_auto()
    
    def publish_data_auto(self):
        try : 
            t = SENSOR.temperature
            h = SENSOR.humidity
            curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            origin_data = {'DEV_ID':'EMS01', 'CURR_DT':curr, 
                            'TEMP': t, 'HUMID':h} #AIRCON
            pub_data = json.dumps(origin_data)
            self.client.publish(topic = 'ems/rasp/data/',
                                payload = pub_data)
            print(f'{curr} -> MQTT Published')
        except RuntimeError as e :
            print(f'ERROR > {e.args[0]}')
        
        Timer(2.0, self.publish_data_auto).start()


class subscriber(Thread) : #Thread를 상속받는 클래스
    def __init__(self):
        Thread.__init__(self);
        self.host = '' #local host #추후 변경 #ip
        self.port =   #port 
        print('subscriber 스레드 시작')
        self.client = mqtt.Client(client_id = 'EMS91')

    def onConnect(self, mqttc, obj, flags, rc):
        print(f'sub : connected with rc > {rc}')

    def onMessage(self, mqttc, obj, msg):
        rcv_msg = str(msg.payload.decode('utf-8'))
        print(f'{msg.topic}/{rcv_msg}')
        data = json.loads(rcv_msg)
        type = data['TYPE']
        stat = data['STAT']
        # print(data['TYPE'])
        # print(data['STAT'])

        if type == 'AIRCON' and stat == 'ON':
            GPIO.output(RED, GPIO.HIGH)
        elif type == 'AIRCON' and stat =='OFF':
            GPIO.output(RED, GPIO.LOW)

        if type == 'DEHUMD' and stat == 'ON':
            GPIO.output(BLUE, GPIO.HIGH)
        elif type == 'DEHUMD' and stat =='OFF':
            GPIO.output(BLUE, GPIO.LOW)
        
        time.sleep(1.0)

    def run(self):
        GPIO.output(RED, GPIO.HIGH)
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.connect(self.host, self.port) 
        self.client.subscribe(topic = 'ems/rasp/control/') #닫는 구간이라, topic이 달라야 한다.
        self.client.loop_forever()


if __name__ == '__main__':
    try : 
        thPub = publisher()
        thSub = subscriber()

        thPub.start()
        thSub.start() 

    except KeyboardInterrupt:
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW)
        GPIO.cleanup()


