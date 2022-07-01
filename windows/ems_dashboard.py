# EMS DASHBOARD APP
import sys
from PyQt5 import uic
from tkinter.messagebox import NO, YES
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import requests
import json
import dashboard_rc # 리소스 py 파일 추가
import paho.mqtt.client as mqtt # mqtt subscribe를 위해서 추가
import time

#pip install PyMySQL
import pymysql

import datetime as dt


#시각화
#pip install pyqtgraph
#pip install pyqtchart
from PyQt5.QtChart import *  #Qtdesigner에서 승격해서 사용 가능


broker_url = 'localhost' #local server에 MQTT broker가 같이 설치되어 있으므로


class Worker(QThread):
    sigStatus = pyqtSignal(str) #연결 상태 시그널, 부모 클래스인 MyApp으로 전달용
    sigMessage = pyqtSignal(dict) #MQTT Subscribe 시그널, MyApp 전달

    def __init__(self, parent) :
        super().__init__(parent)
        self.parent = parent
        self.host = broker_url
        self.port =   #port
        self.client = mqtt.Client(client_id = 'Dashboard')

    def onConnect(self, mqttc, obj, flags, rc):
        try :
            print(f'connected with result code > {rc}')   #접속되었을 때만 데이터를 넘겨받는다.
            self.sigStatus.emit('SUCCEED') #MyApp로 성공 메시지 전달
        except Exception as e:
            print(f'error > {e.args}')
            self.sigStatus.emit('FAILED')


    def onMessage(self, mqttc, obj, msg):
        rcv_msg =str(msg.payload.decode('utf-8'))
        #print(f'{msg.topic}/{rcv_msg}') #시그널로 전달
        self.sigMessage.emit(json.loads(rcv_msg))
        time.sleep(2.0)

    def mqttloop(self):
        self.client.loop()
        print('MQTT client loop')

    def run(self): #Thread 에는 run()이 필수
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.connect(self.host, self.port)
        self.client.subscribe(topic = 'ems/rasp/data/')
        self.client.loop_forever()  #무한반복 (사용자가 종료할 때까지)


class MyApp(QMainWindow):
    isTempAlarmed = False #알람 여부 결정 #항상 False값을 갖는다.
    isHumidAlarmed = False
    tempData = humidData = None  
    idx = 0 #초기화

    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()
        self.showTime()
        self.showWeather()
        self.initThread()
        self.initChart()

    def initChart(self):
        # self.viewLimit = 128 # chart 그릴 개수 제한  
        
        self.tempData = self.humidData = QLineSeries()
        self.iotChart = QChart()

        # axisX = QDateTimeAxis()
        # axisX.setFormat('HH:mm:ss')
        # axisX.setTickCount(5)
        # dt = QDateTime.currentDateTime()
        # axisX.setRange(dt,dt.addSecs(self.viewLimit))

        # axisY = QValueAxis()
        
        self.iotChart = QChart()
        # self.iotChart.addAxis(axisX, Qt.AlignBottom)
        # self.iotChart.addAxis(axisY, Qt.AlignLeft)
        # self.tempData.attachAxis(axisX)
        # self.humidData.attachAxis(axisY)

        self.iotChart.layout().setContentsMargins(5,5,5,5)

        self.dataView.setChart(self.iotChart)
        self.dataView.setRenderHint(QPainter.Antialiasing)
        
    #     self.iotData = QLineSeries()
    
    #     self.iotData.append(0,10)
    #     self.iotData.append(1,20)
    #     self.iotData.append(2,15)
    #     self.iotData.append(3,22)

    #     self.iotChart = QChart()
    #     self.iotChart.addSeries(self.iotData)

    #     self.dataView.setChart(self.iotChart)


    def initThread(self):
        self.myThread = Worker(parent = self)
        self.myThread.sigStatus.connect(self.updateStatus)
        self.myThread.sigMessage.connect(self.updateMessage)
        self.myThread.start()

    @pyqtSlot(dict)
    def updateMessage(self, data): #중요
        # 1. 딕셔너리 분해 작업 (json으로 변환)
        # 2. Label에 Device 명칭 업데이트
        # 3. 온도 Label, 습도 Label에 현재 온도 업데이트
        # 4. MySQL DB에 입력
        # 5. 이상기온 알람
        # 6. txbLog 로그 출력  / 다시 제거
        # 7. Chart 데이터 추가 

        dev_id = data['DEV_ID'] #2.
        self.lblTempTitle.setText(f'{dev_id} Temperature')
        self.lblHumidTitle.setText(f'{dev_id} Humidity')

        temp = data['TEMP']
        humid = data['HUMID']
        self.lblCurrTemp.setText(f'{temp:.1f}')
        self.lblCurrHumid.setText(f'{humid:.0f}')


        #self.txbLog.append(json.dumps(data))
        #self.dialHumid,setValue(int(humid)) 220701 위젯 삭제

        # 5. 이상기온 알람
        if temp >= 27 :  #이상 기온 지정
            self.lblTempAlarm.setText(f'{dev_id} : 이상 기온')
            self.btnTempAlarm.setEnabled(True) #버튼 활성화
            self.btnTempStop.setEnabled(False)

            if self.isTempAlarmed == False: #온도가 정상기온이 되기 전까지 다시 알람이 나오지 않도록 함
                self.isTempAlarmed = True

                QMessageBox.warning(self, '경고',f'{dev_id}에서 이상 기온을 감지하였습니다.')


        elif temp <=26.5 :
            self.lblTempAlarm.setText(f'{dev_id} : 정상 기온')
            self.isTempAlarmed = False
            self.btnTempAlarm.setDisabled(True) #버튼 비활성화
            self.btnTempStop.setEnabled(True)




        if humid >=  60.0 :  #이상 습도 지정
            self.lblHumidAlarm.setText(f'{dev_id} : 이상 습도')
            if self.isHumidAlarmed == False: #온도가 정상기온이 되기 전까지 다시 알람이 나오지 않도록 함
                self.btnHumidAlarm.setEnabled(True)
                QMessageBox.warning(self, '경고',f'{dev_id}에서 이상 습도를 감지하였습니다.')
        elif humid <= 55.0 :
            self.lblHumidAlarm.setText(f'{dev_id} : 정상 습도')
            self.isHumidAlarmed = False



        # 4. DB 입력
        self.conn = pymysql.connect(host = '127.0.0.1', #local host
                                user = 'bms',
                                password = '1234',
                                db = 'bms',
                                charset = 'euckr')
        curr_dt = data['CURR_DT'] #문자열
        query = '''INSERT INTO ems_data
		                (dev_id, curr_dt, temp, humid)
                    VALUES
		                (%s, %s, %s, %s) '''

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, (dev_id, curr_dt, temp, humid))
                self.conn.commit()
                print('DB Inserted!')

        # 7. Chart update
        self.updateChart(curr_dt, temp, humid)

    def updateChart(self, curr_dt, temp, humid):
        self.tempData.append(self.idx, temp)
        self.humidData.append(self.idx, humid)

        self.iotChart.




    @pyqtSlot(str)
    def updateStatus(self, stat):
        if stat == 'SUCCEED':
            self.lblStatus.setText("Connected")
            self.conFrame.setStyleSheet(
                'background-image: url(:/green); '
                'background-repeat: no-repeat; '
                'border:none;'
            )
        else :
            self.lblStatus.setText("Disconnected")
            self.conFrame.setStyleSheet(
                'background-image: url(:/red); '
                'background-repeat: no-repeat; '
                'border:none;'
            )



    def showWeather(self):
        url = '' #url link with allocated key

        result = requests.get(url)
        result = json.loads(result.text)
        weather = result['weather'][0]['main'].lower()  #글자를 전부 소문자로 교체
        self.weatherFrame.setStyleSheet(
            (
                f'background-image: url(:/{weather});'
                'background-repeat: no-repeat;'
                'border:none;'


            )
        )


    def showTime(self):
        #Qt에 있는 시간 사용
        today = QDateTime.currentDateTime()
        currDate = today.date()
        currTime = today.time()
        currDay = today.toString('dddd')

        self.lblDate.setText(currDate.toString('yyyy-MM-dd'))
        self.lblDay.setText(currDay)
        self.lblTime.setText(currTime.toString('HH:mm'))

        if today.time().hour() > 5 and today.time().hour() <= 12:
            self.lblGreeting.setText('Good Morning!')
        elif today.time().hour() >= 12 and today.time().hour() < 18:
            self.lblGreeting.setText('Good Afternoon!')
        elif today.time().hour() >= 18 :
            self.lblGreeting.setText('Good Evening!')
        else :
            self.lblGreeting.setText('Good Night!')




    def initUI(self):
        uic.loadUi('./windows/ui/dashboard.ui',self)
        self.setWindowIcon(QIcon('iot_64.png'))

        #윈도우 정중앙에 화면이 나타나도록 한다.
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft()) # End of screen central position
        self.btnTempAlarm.setDisabled(False) #버튼 비활성화
        self.btnTempStop.setEnabled(True)
        self.btnHumidAlarm.setEnabled(False)


        #위젯 시그널 정의
        self.btnTempAlarm.clicked.connect(self.btnTempAlarmClicked)
        self.btnTempStop.clicked.connect(self.btnTempStopClicked)

        self.btnHumidAlarm.clicked.connect(self.btnHumidAlarmClicked)
        self.btnHumidStop.clicked.connect(self.btnHumidStopClicked)

        self.show()

    def btnHumidAlarmClicked(self):
        QMessageBox.information(self, '알람', '이상 습도 발생, 제습기를 가동합니다.')
        self.client = mqtt.Client(client_id = 'Controller')
        self.client.connect(broker_url, ) #port
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID':'CONTROL', 'CURR_DT':curr,
                        'TYPE': 'DEHUMD', 'STAT':'ON'} #DEHUMD
        pub_data = json.dumps(origin_data)
        self.client.publish(topic = 'ems/rasp/control/',
                            payload = pub_data)
        print('Dehumidifier On Published')
        self.insertAlarmData('CONTROL',curr,'DEHUMD','ON' )


    def btnHumidStopClicked(self):
        QMessageBox.information(self, '정상', '제습기 작동을 중지합니다.')
        self.client = mqtt.Client(client_id = 'Controller')
        self.client.connect(broker_url, ) #port
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID':'CONTROL', 'CURR_DT':curr,
                        'TYPE': 'DEHUMD', 'STAT':'OFF'} #DEHUMD
        pub_data = json.dumps(origin_data)
        self.client.publish(topic = 'ems/rasp/control/',
                            payload = pub_data)
        print('Dehumidifier Off Published')
        self.insertAlarmData('CONTROL',curr,'DEHUMD','OFF' )


    def btnTempAlarmClicked(self):
        QMessageBox.information(self, '알람', '이상 온도 발생, 에어컨을 가동합니다.')
        self.client = mqtt.Client(client_id = 'Controller')
        self.client.connect(broker_url, ) #port
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID':'CONTROL', 'CURR_DT':curr,
                        'TYPE': 'AIRCON', 'STAT':'ON'} #AIRCON
        pub_data = json.dumps(origin_data)
        self.client.publish(topic = 'ems/rasp/control/',
                            payload = pub_data)
        print('Airconditioner On Published')
        self.insertAlarmData('CONTROL',curr,'AIRCON','ON' )


    def btnTempStopClicked(self):
        QMessageBox.information(self, '정상', '에어컨 작동을 중지합니다.')
        self.client = mqtt.Client(client_id = 'Controller')
        self.client.connect(broker_url, ) #port
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID':'CONTROL', 'CURR_DT':curr,
                        'TYPE': 'AIRCON', 'STAT':'OFF'} #AIRCON
        pub_data = json.dumps(origin_data)
        self.client.publish(topic = 'ems/rasp/control/',
                            payload = pub_data)
        print('AIRCON Off Published')
        self.insertAlarmData('CONTROL',curr,'AIRCON','OFF' )


    def insertAlarmData(self, dev_id, curr_dt, types, stat): #type이 파이썬에 있어서 명칭 조정
        self.conn = pymysql.connect(host = '127.0.0.1', #local host
                                user = 'bms',
                                password = '1234',
                                db = 'bms',
                                charset = 'euckr')
        query = '''INSERT INTO ems_alarm
		                (dev_id, curr_dt, type, stat)
                    VALUES
		                (%s, %s, %s, %s) '''

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, (dev_id, curr_dt, types, stat))
                self.conn.commit()
                print('Alarm Inserted!')

    # 종료 메세지 박스
    def closeEvent(self, signal):
        ans = QMessageBox.question(self, '종료', '종료 하시겠습니까?',
                                    QMessageBox.Yes| QMessageBox.No,
                                    QMessageBox.No)
        if ans == QMessageBox.Yes:
            signal.accept()
        else:
            signal.ignore()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()
