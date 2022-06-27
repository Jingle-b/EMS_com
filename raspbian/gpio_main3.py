## PUSHBUTTON RGB LED Control


# BUTTON PUSH EVENT
# 스위치를 통한 제어

import RPi.GPIO as GPIO
import time

BUTTON = 3
RED = 11
GREEN  = 12
BLUE = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON, GPIO.IN) #event를 함수 사용하는 형태로 
GPIO.setup(RED,GPIO.OUT) #11핀에 출력세팅
GPIO.setup(GREEN, GPIO.OUT) #12핀에 출력세팅
GPIO.setup(BLUE,GPIO.OUT) #13핀에 출력세팅

is_click = False  #변수 초기화 

def button_push(val):
    global is_click 
    if is_click == True : #초기값이 False라서, 처음 입력이 제대로 작용하지 않았던 문제 발생(4번에서 해결 완료)
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.HIGH) 
    else : 
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW) 
    is_click = not is_click #실행될 때마다 값을 바꾼다.


while True :
    GPIO.wait_for_edge(BUTTON, GPIO.RISING, bouncetime = 100)
    time.sleep(0.1) #time.sleep을 통해, signal을 받을 시간을 준다. 

    button_push(GPIO.input(BUTTON))  #스위치를 누르면 신호가 발생한다. 

