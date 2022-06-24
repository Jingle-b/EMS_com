## QLabel 위젯
import sys
from PyQt5.QtWidgets import * #QApplication, QWidget, QLabel, QHBoxLayout 사용 #QHBoxLayout - 가로로 된 박스 레이아웃
from PyQt5.QtGui import * #QPainter, QColor, QFont 사용 #위젯아닌 속성
from PyQt5.QtCore import * #Qt 사용 #Core 속성

class MyApp(QWidget):

    def __init__(self) -> None :
        super().__init__()
        self.initUI()    

    def initUI(self):
        self.setWindowTitle('PyQt QLabel') 
        self.setGeometry(600,250,300,300)
        self.setWindowIcon(QIcon('lion.png')) #아이콘 추가

        #Label 작업 시작
        label1, label2 = QLabel('Label1'), QLabel('라벨2') #괄호 안에 '문자열' 입력하면 레이아웃에 글자가 들어간다.
        label1.setAlignment(Qt.AlignBottom)
        label1.setStyleSheet(
            ('border-width : 3px;'
             'border-style : solid;' #실선
             'border-color : blue;'
             'image: url(./windows/images/image1.png)'
            )
        )    
        label2.setAlignment(Qt.AlignBottom)
        label2.setStyleSheet(
            ('border-width : 3px;'
             'border-style : dot-dot-dash;' #실선
             'border-color : red;'
             'image: url(./windows/images/image2.png)'
            )
        )

        hbox = QHBoxLayout(self) #레이아웃은 보이지 않음
        #addWidget해서 추가하면 자동으로 나뉘어진다.(균등하게)
        hbox.addWidget(label1)  #하나 레이아웃에 라벨1
        hbox.addWidget(label2) #두번째 레이아웃에 라벨2 들어감 


        self.show()

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    
    app.exec_()

