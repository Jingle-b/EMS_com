# 스레드 없이 동작
# PyQt5 템플릿 소스 
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyApp(QWidget): 
    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./windows/ui/threadtask.ui',self) 
        self.btnStart.clicked.connect(self.btnStartClicked)
        self.show()

    # 핵심 logic 
    def btnStartClicked(self):
        self.pgbTask.setRange(0,99) #0~99 
        for i in range(0,100):  #0~99   
            #범위를 둘 다 0~9999로 설정할 경우, ui 스레드의 단점이 나타난다. (큰 일을 처리해야 할 때, 중간에 응답없음 나타남)
            print(f'출력 > {i}')
            self.pgbTask.setValue(i)
            self.txbLog.append(f'출력 > {i}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()