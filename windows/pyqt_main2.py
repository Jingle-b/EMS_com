## PyQt 클래스화 / PyQt 템플릿

import sys
from PyQt5.QtWidgets import QApplication, QWidget

class MyApp(QWidget):

    def __init__(self) -> None : #return 값이 없음 (생략 가능한 구문 : ->None)
        super().__init__()
        self.initUI()    #내가 만들 ui를 완전 초기화한다. 

    def initUI(self): #class안에 있는 함수는 반드시 self를 파라미터 위치에 넣어야 한다. 
        self.setWindowTitle('PyQt Widget2') #헤더 
    
        self.setGeometry(600,250,300,300)
        '''  
        // setGeometry는 이 두 줄의 코드의 기능을 합친 것 !
        self.move(600,250) #생성하는 윈도우 창의 위치 설정  - 중앙에 놓고싶으면 따로 코드 이용 or 계산해서 위치시킴 
        self.resize(300,300)
        ''' 
        self.show()

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    
    app.exec_()

