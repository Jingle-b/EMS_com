## PYQT 학습
from PyQt5.QtWidgets import *  #import all 
import sys 


def run():  #기본 폼
    #앱 생성
    app = QApplication(sys.argv) #1. app 객체 생성

    #앱 내용 
    wnd = QMainWindow() #2. window 객체 생성 - QWidget, QMainWindow, QDialog도 있다. 
    label = QLabel('\tHello, Qt5!!') #라벨 위젯 생성
    wnd.setWindowTitle('First PyQt')
    wnd.resize(500,300)  #qt designer 사용하면 이렇게 조정 안해도 된다. 
    wnd.setCentralWidget(label) 
    wnd.show() #3.

    #앱 실행
    app.exec_() #4. 


'''
from PyQt5 import QtWidgets 형식으로 import하는 경우

def run():  #기본 폼
    app = QtWidgets.QApplication([]) #1. app 객체 생성  # [] = 빈 리스트 (sys import 안했을 때 사용했음)
    wnd = QtWidgets.QMainWindow() #2. window 객체 생성
    label = QtWidgets.QLabel('\tHello, Qt5!!') #라벨 위젯 생성
    wnd.setCentralWidget(label) 
    wnd.show() #3.
    app.exec_() #4. 

'''


if __name__ == '__main__':
    run()
