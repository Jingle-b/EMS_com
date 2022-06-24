## QFont 속성 사용 
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont #위젯아닌 속성
from PyQt5.QtCore import Qt #Core 속성

class MyApp(QWidget):

    def __init__(self) -> None :
        super().__init__()
        self.initUI()    

    def initUI(self): 
        self.setWindowTitle('QFont test')
        self.setGeometry(600,250,300,300)
        self.text = 'Test Message'
        self.show()
    
    def paintEvent(self, signal):
        paint = QPainter(self)
        paint.begin(self)
        self.drawText(signal, paint)
        paint.end()

    def drawText(self, signal, paint):
        paint.setPen(QColor(100,100,255)) #RGB 색상 (0~255) 
        paint.setFont(QFont('Impact',20))
        paint.drawText(105, 100, "Hello Qt!")
        paint.setPen(QColor(100,100,100)) 
        paint.setFont(QFont('Arial',16))
        paint.drawText(signal.rect(), Qt.AlignCenter, self.text) #initUI 에서 입력된 self.text 문자열
        #initUI 에서 입력된 self.text 문자열 #AlignCenter = 정중앙에 위치시키겠다. 
        



    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    
    app.exec_()

