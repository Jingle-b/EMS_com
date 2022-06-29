# MQTT Publisher 
# sudo pip install paho-mqtt 
import threading 
import datetime as dt
import paho.mqtt.client as mqtt 
import json

client2  = None 
count = 0

def publish_sensor_data():
    curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    #dictionary
    origin_data = { 'DEV_ID' : 'EMS07', 'CURRENT_DT': curr,
                    'TEMP(`C)' : 25.4, 'HUMID(%)' : 60}     #templete (예시 데이터)
    pub_data = json.dumps(origin_data)
    client2.publish(topic = 'ems/rasp/data/', #publish 인자 - topic : 내가 원하는 주제 - 책의 topic과 같은 개념! 중요 
                    payload =pub_data)

    print(f'{curr} -> MQTT Published')

    threading.Timer(2.0,publish_sensor_data).start() #2초마다 publish_sensor_data 실행 


    



if __name__ == '__main__':
    broker_url = '' #ip address 
    client2 = mqtt.Client(client_id = 'EMS07') 
    client2.connect(host=broker_url, 
                    port = ) #port  

    publish_sensor_data()


