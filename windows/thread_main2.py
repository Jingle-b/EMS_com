# 스레드 없이 동작
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#Background work
#스레드
class Worker(QThread) : # PyQt에서 스레드 사용
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent #윈도우 클래스에 

    
    def run(self):
        #스레드로 동작할 내용이 작성될 부분
        self.parent.pgbTask.setRange(0,99) #0~99 
        for i in range(0,100):  #0~99   
            print(f'출력 > {i}')
            self.parent.pgbTask.setValue(i)
            self.parent.txbLog.append(f'출력 > {i}')



#프로세스
class MyApp(QWidget): 
    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./windows/ui/threadtask.ui',self) 
        self.btnStart.clicked.connect(self.btnStartClicked)
        self.show()

    def btnStartClicked(self): 
        th = Worker(self) #Worker 의 부모가 MyApp임을 밝힘
        th.start()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()