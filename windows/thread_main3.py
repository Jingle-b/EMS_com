# 스레드 사용 / 커스텀 시그널 동작 (완성본)
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time 


#Background work
#스레드
class Worker(QThread) : # PyQt에서 스레드 사용
    valChangeSignal = pyqtSignal(int) #전달받을 값이 int이다. 

    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.working = True

    
    def run(self):
        #스레드로 동작할 내용이 작성될 부분
        #self.parent.pgbTask.setRange(0,99) #0~99 
        while self.working : 
            for i in range(0,10000):  #0~9999   
                print(f'출력 > {i}')
                #(변경사항) 기존 코드를 실행하는 대신, 커스텀 시그널에 보내서 부모 클래스에서 받아서 처리하도록 한다.
                self.valChangeSignal.emit(i)  
                time.sleep(0.0001)  #안전망 - 시간은 좀 느려지지만, 응답없음이 나타나지 않도록 함!  
                #그리고 time.sleep을 없애는 경우, 간혹 100%에서 멈춰지지 않는 경우 발생. [예외 발생!] 

                #기존 코드
                #self.parent.pgbTask.setValue(i)
                #self.parent.txbLog.append(f'출력 > {i}')



#프로세스
class MyApp(QWidget): 
    #setValueSignal = pyqtSignal() -> worker로 보낼 signal이 없으므로, MyApp에서는 필요 없다. 

    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./windows/ui/threadtask.ui',self) 
        self.btnStart.clicked.connect(self.btnStartClicked)
        #(변경사항) Worker 클래스가 가지고 있는 valueChangeSignal 설정
            #Worker 의 부모가 MyApp임을 밝힘
        self.th = Worker(parent  = self) # Worker(self)와 같은 의미

        #workerValChanged = Worker에 있는 valChangeSignal에 대한 슬롯 정의  
        self.th.valChangeSignal.connect(self.updateProgress) 

        self.show()

    @pyqtSlot(int) #<- decorator[장식] : pyqt의 슬롯임을 의미하는 장식 (int = 슬롯이 받는 파라미터의 자료형) - 커스텀 슬롯임을 알림 
    def updateProgress(self, val):
        self.pgbTask.setValue(val)
        self.txbLog.append(f'출력 > {val}')
        if val == 9999:
            self.th.working = False 


    @pyqtSlot() 
    def btnStartClicked(self): 
        self.pgbTask.setRange(0,9999)
        self.th.start()
        self.th.working = True



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()