import RPi.GPIO as GPIO
import time

CLK = 37
DT = 38
SW = 40

globalCounter = 0

flag = 0
Last_DT_Status = 0
Current_DT_Status = 0

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(CLK, GPIO.IN)
    GPIO.setup(DT, GPIO.IN)
    GPIO.setup(SW, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    
def rotaryDeal():
    global flag
    global Last_DT_Status
    global Current_DT_Status
    global globalCounter
    Last_DT_Status = GPIO.input(DT)
    while not GPIO.input(CLK) :
        Current_DT_Status = GPIO.input(DT)
        flag = 1
    if flag == 1:
        flag = 0
        if Last_DT_Status == 1 and Current_DT_Status == 0:
            globalCounter = (globalCounter + 1)%35
        if Last_DT_Status == 0 and Current_DT_Status == 1:
            globalCounter = (globalCounter - 1)%35
            
def btnISR(channel):
    global globalCounter
    print('button click')
    globalCounter = 0
    
def loop():
    global globalCounter
    tmp = 0
    GPIO.add_event_detect(SW, GPIO.FALLING, callback=btnISR)
    while True:
        rotaryDeal()
        if tmp != globalCounter:
            print('globalCounter = %d' % globalCounter)
            tmp = globalCounter
            
def destroy():
    GPIO.cleanup()
    
if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
    
    