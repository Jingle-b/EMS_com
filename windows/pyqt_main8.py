## Signal & Plot 
import sys
from PyQt5.QtWidgets import * #import All 
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyApp(QWidget):

    def __init__(self) -> None :
        super().__init__()
        self.initUI()    

    def initUI(self): 
        self.setWindowTitle('Signal')
        self.setGeometry(490,250,300,300)
        self.setWindowIcon(QIcon('/lion.png')) #아이콘 추가

        self.label = QLabel(self)
        self.setFont(QFont('Arial',15))
        self.label.setText('LED OFF')

        self.btn = QPushButton('LED ON', self)
        
        #시그널 정의 
        self.btn.clicked.connect(self.btn_clicked)
    
        #화면 구성
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.label)
        vbox.addWidget(self.btn)

        self.show()
    
    def btn_clicked(self):
        self.label.setText('LED ON')
        # raspberry pi GPIO ON


    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    
    app.exec_()

