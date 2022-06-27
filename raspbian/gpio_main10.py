#Distance Sensor test
from errno import EHOSTDOWN
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) 

TRIG = 16
ECHO = 18

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, GPIO.LOW)
print('Init Ultrasonic')
time.sleep(2.0)

try :
    while True:
        GPIO.output(TRIG, GPIO.HIGH)
        time.sleep(0.00001) #10 us Delay 
        GPIO.output(TRIG, GPIO.LOW)

        while GPIO.input(ECHO) == 0:
            start = time.time()

        while GPIO.input(ECHO) == 1:
            stop = time.time()

        check_time = stop - start
        distance = check_time * 34300/2     #거리
        print(f'Distance = {distance: .1f} cm')
        time.sleep(0.4)
    
except KeyboardInterrupt:
    GPIO.cleanup()
