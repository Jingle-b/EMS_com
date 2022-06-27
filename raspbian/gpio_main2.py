# BUTTON PUSH EVENT
# 스위치를 통한 제어

import RPi.GPIO as GPIO
import time

BUTTON = 3
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON, GPIO.IN)

while True :
    GPIO.wait_for_edge(BUTTON, GPIO.RISING, bouncetime = 100)
    time.sleep(0.1) #time.sleep을 통해, signal을 받을 시간을 준다. 

    print(GPIO.input(BUTTON))  #스위치를 누르면 신호가 발생한다. 
