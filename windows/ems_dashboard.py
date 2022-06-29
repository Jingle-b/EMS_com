# EMS DASHBOARD APP
# 데이터 제공 - 기상청 공공데이터 포털 
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import requests
import json

import dashboard_rc # 리소스 py 파일 추가 

class MyApp(QMainWindow):

    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()
        self.showTime()
        self.showWeather()

    def showWeather(self):
        url = '' #url link with allocated key

        result = requests.get(url)
        result = json.loads(result.text)
        weather = result['weather'][0]['main'].lower()  #글자를 전부 소문자로 교체
        self.weatherFrame.setStyleSheet(
            (
                f'background-image: url(:/{weather});'
                'backgroud-repeat: no-repeat;'
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
        self.show()


    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()
