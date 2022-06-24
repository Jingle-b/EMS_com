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

        btn1 = QPushButton('Click1', self)
        btn2 = QPushButton('Click2', self)
        btn3 = QPushButton('Click3', self)
        btn4 = QPushButton('Click4', self)
        btn5 = QPushButton('Click5', self)
        btn6 = QPushButton('Click6', self)
        #btn1.setGeometry(50,100,100,40) #레이아웃에 할당하면 사이즈 조정 불가 - 레이아웃 사이즈에만 맞게 입력됨
        #레이아웃은 자유롭게 구성할 수 있다. 
        # QHBox Layout, QVBoxLayout, QGridLayout
        vbox = QGridLayout(self)
        vbox.addWidget(btn1, 0,0 )
        vbox.addWidget(btn2, 0,1)
        vbox.addWidget(btn3, 0,2)
        vbox.addWidget(btn4, 1,0)
        vbox.addWidget(btn5, 1,1)
        vbox.addWidget(btn6, 1,2)

        self.show()
    


    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    
    app.exec_()

