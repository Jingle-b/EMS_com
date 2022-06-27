## PUSHBUTTON RGB LED Control v2 


import RPi.GPIO as GPIO
import time

BUTTON = 3
RED = 11
GREEN  = 12
BLUE = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #button click에 대한 반응(pull up down에 대한 설정)
GPIO.setup(RED,GPIO.OUT) #11핀에 출력세팅
GPIO.setup(GREEN, GPIO.OUT) #12핀에 출력세팅
GPIO.setup(BLUE,GPIO.OUT) #13핀에 출력세팅

is_click = False
count = 0



def button_push(channel):
    global count
    if count % 5 == 1 : #red 
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW) 
    
    elif count % 5 == 2: #green
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.LOW)  

    elif count % 5 == 3: #blue
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.HIGH)

    elif count % 5 == 4: #white
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.HIGH)

    else: #out
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW)

    count += 1

    ''' #기존 코드 
    global is_click
    print('Button pushed!')
    if is_click == False : #False = 꺼져있음
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.HIGH) 
    else : 
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW) 
    
    is_click = not is_click 
    '''

GPIO.add_event_detect(BUTTON, GPIO.RISING, 
                      callback = button_push, 
                      bouncetime = 100)


try : 
    while True : time.sleep(0.1)
except KeyboardInterrupt :
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(BLUE, GPIO.LOW)
    GPIO.cleanup()