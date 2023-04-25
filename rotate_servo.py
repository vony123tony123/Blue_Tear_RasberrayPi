import RPi.GPIO as GPIO
import time
import pigpio
import requests


CLK = 8
DT = 10
#SW = 40
control = 18
pwm_f = 50 


servo_Counter = 0
flag = 0
Last_DT_Status = 0
Current_DT_Status = 0
pi = pigpio.pi()

url = "http://192.168.100.124:30000/post_json"

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(control,GPIO.OUT)
    GPIO.setup(CLK, GPIO.IN)
    GPIO.setup(DT, GPIO.IN)
    pi.set_mode(control,pigpio.INPUT)
    pi.hardware_PWM(control,pwm_f,angle_to_duty_cycle(0))
    #GPIO.setup(SW, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    
    
def rotaryDeal():
    global flag
    global Last_DT_Status
    global Current_DT_Status
    global servo_Counter
    Last_DT_Status = GPIO.input(DT)
    while not GPIO.input(CLK) :
        Current_DT_Status = GPIO.input(DT)
        flag = 1
    if flag == 1:
        flag = 0
        if Last_DT_Status == 1 and Current_DT_Status == 0 and servo_Counter <72 :#clock wise
            servo_Counter = servo_Counter + 1
        if Last_DT_Status == 0 and Current_DT_Status == 1 and servo_Counter >0 :#reverse clock wise
            servo_Counter = servo_Counter - 1

def angle_to_duty_cycle(angle=0):
    duty_cycle = int((500*pwm_f)+(1900*pwm_f*angle / 180))
    return duty_cycle

def servo_move():
    global servo_Counter
    angle = 5 * servo_Counter
    dc = angle_to_duty_cycle(angle)
    pi.hardware_PWM(control,pwm_f,dc)
    print('angle = {: >3}, work cycle={:.2f}'.format(angle,dc))
#def btnISR(channel):
    #global servo_Counter
    #print('button click')
    #servo_Counter = 0
    
def loop():
    global servo_Counter
    tmp = 0
    #GPIO.add_event_detect(SW, GPIO.FALLING, callback=btnISR)
    while True:
        rotaryDeal()
        if tmp != servo_Counter:
            print('servo_Counter = %d' % servo_Counter)
            #requests.post(url, json={"key":100})
            servo_move()
            tmp = servo_Counter
            
def destroy():
    print("Close")
    #pi.hardware_PWM(control,pwm_f,angle_to_duty_cycle(0))
    #pi.set_mode(control,pigpio.INPUT)
    GPIO.cleanup()
    
    #pi.set_mode(control,pigpio.INPUT)
    
if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
    
    
