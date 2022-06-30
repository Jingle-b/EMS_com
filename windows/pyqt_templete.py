# PyQt5 템플릿 소스 
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyApp(QWidget): #QtMainWindow로 변경 필요
    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./windows/ui/navermovie.ui',self)  #UI 파일 변경 요
        #To do  - 로직은 이곳에 작성
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()