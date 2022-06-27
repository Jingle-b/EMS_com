#RGB LED ON/OFF
import RPi.GPIO as GPIO #Raspberry Pi i 
import time

#브레드보드 위치
RED = 11
GREEN  = 12
BLUE = 13

GPIO.setmode(GPIO.BOARD) #보드 번호 기준(1~40) #다른 기준 : GPIO.BCM
GPIO.setup(RED,GPIO.OUT) #11핀에 출력세팅
GPIO.setup(GREEN, GPIO.OUT) #12핀에 출력세팅
GPIO.setup(BLUE,GPIO.OUT) #13핀에 출력세팅

'''
# 하나만 보고싶을때
#GPIO.output(RED, GPIO.HIGH) #불이 켜지면 프로그램 종료
GPIO.output(RED, GPIO.LOW) #불이 꺼지면 프로그램 종료
'''


try : #파이썬 코드가 실행종료되더라도 계속 불이 켜져있는 예외 처리
    while True: 
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW) #red를 켜는 동안에는 green과 blue를 off
        time.sleep(0.5)

        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.LOW) #green를 켜는 동안에는 red와 blue를 off
        time.sleep(0.5)

        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.HIGH) #blue를 켜는 동안에는 green과 red를 off
        time.sleep(0.5)

        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.HIGH) #전부 on 
        time.sleep(0.5)
    
except KeyboardInterrupt: #keyboardinterrupt가 일어나면 모두 low 처리 
    GPIO.output(RED,GPIO.LOW)
    GPIO.output(GREEN,GPIO.LOW)
    GPIO.output(BLUE,GPIO.LOW)
    GPIO.cleanup()
