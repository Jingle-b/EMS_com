# Servo Motor test
# 01. 0도의 위치 찾기 
import RPi.GPIO as GPIO
import time 
 

SERVO = 12

GPIO.setmode(GPIO.BOARD) #BOARD 로 설정해서 servo 값을 12를 입력해야 한다. 
GPIO.setup(SERVO, GPIO.OUT)

pwm = GPIO.PWM(SERVO, 50) #50Hz servo motor 동작 주파수
#주는 값에 따라 달라진다. 
pwm.start(3.0) #0.6ms

time.sleep(2.0) #2s
pwm.ChangeDutyCycle(0.0)    #0도에 멈춘다.

pwm.stop()
GPIO.cleanup()