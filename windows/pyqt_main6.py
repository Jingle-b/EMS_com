## QPushButton
import sys
from PyQt5.QtWidgets import * #import All 
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyApp(QWidget):

    def __init__(self) -> None :
        super().__init__()
        self.initUI()    

    def initUI(self): 
        self.setWindowTitle('QPushButton test')
        self.setGeometry(490,250,300,300)
        self.setWindowIcon(QIcon('./windows/images/lion.png')) #아이콘 추가
    
        #self.btn1 = btn1 
        btn1 = QPushButton('Hello', self)
        #btn1.setEnabled(False) #버튼 사용여부 결정 가능 (True가 default)
        btn1.clicked.connect(self.btn1_click) #시그널 #클릭하면 함수 연결해줌 - 클릭에 대한 시그널

        vbox = QVBoxLayout(self)
        vbox.addWidget(btn1)

        self.show()
    
    def btn1_click(self): #슬롯 : 시그널을 처리하는 함수 
        QMessageBox.about(self, 'greeting', 'Hi, Everyone')

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    
    app.exec_()

