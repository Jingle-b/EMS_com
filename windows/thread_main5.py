## 동시에 두 가지 task 수행
from threading import Thread, Timer
import time 
import datetime as dt 
import paho.mqtt.client as mqtt
import json


class publisher(Thread) : #Thread를 상속받는 클래스
    def __init__(self):
        Thread.__init__(self)
        self.host = '127.0.0.1' #local host #추후 변경 #ip
        self.port =  #port 
        self.client = mqtt.Client(client_id = 'EMS101')
        print('Publisher 스레드 시작')

    def run(self):
        self.client.connect(self.host,self.port)
        self.publish_data_auto()
    
    def publish_data_auto(self):
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID':'DASHBOARD', 'CURR_DT':curr, 
                        'TYPE': 'DEHUMD', 'STAT':'ON'} #AIRCON
        pub_data = json.dumps(origin_data)
        self.client.publish(topic = 'ems/rasp/control/',
                            payload = pub_data)
        print('Published')
        Timer(3.0, self.publish_data_auto).start()


class subscriber(Thread) : #Thread를 상속받는 클래스
    def __init__(self):
        Thread.__init__(self);
        self.host = '127.0.0.1' #local host #추후 변경 #ip
        self.port =  #port 
        print('subscriber 스레드 시작')
        self.client = mqtt.Client(client_id = 'EMS101')

    def onConnect(self, mqttc, obj, flags, rc):
        print(f'sub : connected with rc > {rc}')

    def onMessage(self, mqttc, obj, msg):
        rcv_msg = str(msg.payload.decode('utf-8'))
        print(f'{msg.topic}/{rcv_msg}')
        time.sleep(2.0)

    def run(self):
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.connect(self.host, self.port) 
        self.client.subscribe(topic = 'ems/rasp/data/')
        self.client.loop_forever()



if __name__ == '__main__':
    thPub = publisher()
    thSub = subscriber()

    thPub.start()
    thSub.start() 