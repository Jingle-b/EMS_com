## QSlider, QDial
import sys
from PyQt5.QtWidgets import * #import All 
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyApp(QWidget):

    def __init__(self) -> None :
        super().__init__()
        self.initUI()    

    def initUI(self): 
        self.setWindowTitle('QSlider and QDial')
        self.setGeometry(490,250,300,300)
        self.setWindowIcon(QIcon('/lion.png')) #아이콘 추가

        #슬라이더
        self.slider = QSlider(Qt.Horizontal, self) 
        self.slider.setRange(0,50)
        self.slider.setSingleStep(2)
        self.slider.setTickPosition(1) #1은 위로 눈금, 2는 아래로 눈금, 3은 위 아래 전부 나옴

        #다이얼
        self.dial = QDial(self)
        self.dial.setRange(0,50)
        self.dial.setSingleStep(5)

        self.btn = QPushButton('Reset', self)

        #시그널 정의 - value change에 대한 반응 (다이얼, 슬라이더를 통해서 값이 바뀌었을 때 변화를 일으킴)
        #self.slider.valueChanged.connect(self.dial.setValue)
        #self.dial.valueChanged.connect(self.slider.setValue)
       
        self.slider.valueChanged.connect(self.slider_changed)
        self.dial.valueChanged.connect(self.dial_changed)
        self.btn.clicked.connect(self.btn_clicked)
    
        #화면 구성
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.slider)
        vbox.addWidget(self.dial)
        vbox.addWidget(self.btn)

        vbox = QVBoxLayout(self)

        self.show()
    
    def slider_changed(self):
        val = self.slider.value()
        self.dial.setValue(val)

    def dial_changed(self):
        val = self.dial.value()
        self.dial.setValue(val)

    def btn_clicked(self):
        self.slider.setValue(0)
        self.dial.setValue(0)


    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    
    app.exec_()

