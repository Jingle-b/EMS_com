# Servo Motor test
import RPi.GPIO as GPIO
import time 
 

SERVO = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SERVO, GPIO.OUT)

pwm = GPIO.PWM(SERVO, 50) #50Hz
pwm.start(3.0) #0.6ms

for cnt in range(0,3):  #3번 하고 멈춤
    pwm.ChangeDutyCycle(3.0) #0도 회전 
    time.sleep(0.5)
    pwm.ChangeDutyCycle(7.5) #90도 회전 
    time.sleep(0.5)
    pwm.ChangeDutyCycle(12.5) #180도 회전
    time.sleep(0.5)

pwm.ChangeDutyCycle(0.0) #초기화
pwm.stop()
GPIO.cleanup()