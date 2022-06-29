# MQTT Publisher 
# sudo pip install paho-mqtt 
#mqtt_main2에서 import 한 사항 
import threading 
import datetime as dt
import paho.mqtt.client as mqtt 
import json

#gpio_main12에서 import 한 사항 
import adafruit_dht as dht
import board

client2  = None 
count = 0
SENSOR = dht.DHT11(board.D4) #gpio 기준 4번


def publish_sensor_data():
    try:
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        t = SENSOR.temperature
        h = SENSOR.humidity
        
        #dictionary
        origin_data = { 'DEV_ID' : 'EMS07', 'CURR_DT': curr,
                        'TEMP' : t, 'HUMID' : h}     #templete (예시 데이터)
                        # 표기는 데이터를 받아서 처리하는 쪽에서 처리할 사항
        pub_data = json.dumps(origin_data)
        client2.publish(topic = 'ems/rasp/data/', #publish 인자 - topic : 내가 원하는 주제 - 책의 topic과 같은 개념! 중요 
                        payload =pub_data)

        print(f'{curr} -> MQTT Published')

    except RuntimeError as e : #Runtime error -> publish X
        print(f'ERROR > {e.args[0]}')
    
    threading.Timer(2.0,publish_sensor_data).start() #2초마다 publish_sensor_data 실행 

    



if __name__ == '__main__':
    broker_url = '' #ip address 
    client2 = mqtt.Client(client_id = 'EMS07') 
    client2.connect(host=broker_url, 
                    port = ) #port 

    publish_sensor_data()


