#QtDesigner 디자인 연동 
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

class MyApp(QMainWindow):  #PyQt 디자인 할 때 MainWindow로 했음 - 영향이 있다!
    
    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):   #UI를 이미 Qt Designer로 만들어서, 쉽게 적용 가능하다. 
        uic.loadUi('./windows/ui/testwin.ui',self) #경로 주의!(시작하는 폴더를 잘 인지하자)

        #signal 작업 
        self.dial.valueChanged.connect(self.dial_Changed) 

        self.show()
    
    def dial_Changed(self):
        self.label.setText(str(self.dial.value()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()



