# Custom Signal & Slot
# 커스텀 시그널로 실행
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyApp(QWidget): #QtMainWindow로 변경 필요
    closeSignal = pyqtSignal() #커스텀 시그널

    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Close Demo')
        self.resize(300,300)
        
        self.btnClose = QPushButton('close', self)
        self.btnClose.clicked.connect(self.btnCloseClicked)
        self.closeSignal.connect(self.onClose) # btnCloseClicked 실행 했을 때, closeSignal이 연결해서 기능을 수행함 (브로커 느낌)

        self.show()

    def btnCloseClicked(self):
        self.closeSignal.emit() #커스텀 시그널을 실행시킨다. 
    
    def onClose(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()