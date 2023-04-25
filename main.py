import RPi.GPIO as GPIO
import time
import pigpio
import requests

sw = 17#11
R = 22#15
G = 27#13
B = 23#16

CLK = 14#8`
DT = 15#10
SW = 21#40

#servo servo_control
servo_control = 18#12
fan_angle_control = 19
pwm_f = 50

fan_Counter = 0  
servo_Counter = 0
globalCounter = 0

flag = 0
Last_DT_Status = 0
Current_DT_Status = 0

colors = list()
preview_color= 0;
num_colors = 0

pi = pigpio.pi()

url = "http://140.115.51.186:6200"

pwm = 0


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sw, GPIO.OUT)
    GPIO.setup(R, GPIO.OUT)
    GPIO.setup(G, GPIO.OUT)
    GPIO.setup(B, GPIO.OUT)
    GPIO.setup(CLK, GPIO.IN)
    GPIO.setup(DT, GPIO.IN)
    GPIO.setup(SW, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    #servo
    GPIO.setup(servo_control,GPIO.OUT)
    pi.set_mode(servo_control,pigpio.INPUT)
    pi.hardware_PWM(servo_control,pwm_f,angle_to_duty_cycle(3))
    
def setupPWM(freq, dc):
    pwm_r = GPIO.PWM(R, freq)
    pwm_b = GPIO.PWM(B, freq)
    pwm_g = GPIO.PWM(G, freq)
    pwm_r.start(dc)
    pwm_g.start(dc)
    pwm_b.start(dc)
    return pwm_r, pwm_g, pwm_b
        
def PWM(R_value, G_value, B_value):
    pwm_r.ChangeDutyCycle(R_value)
    pwm_g.ChangeDutyCycle(G_value)
    pwm_b.ChangeDutyCycle(B_value)
    #time.sleep(0.1)
    
def close():
    print("Close")
    GPIO.output(sw, GPIO.LOW)
    GPIO.output(R, GPIO.LOW)
    GPIO.output(G, GPIO.LOW)
    GPIO.output(B, GPIO.LOW)
    GPIO.cleanup()

def colorChange(start, end, steps):
    if (end[0]-start[0])//steps != 0:
        r_range = list(range(start[0], end[0], (end[0]-start[0])//steps))
    else:
        r_range = [start[0] for _ in range(steps)]
        
    if (end[1]-start[1])//steps != 0:
        g_range = list(range(start[1], end[1], (end[1]-start[1])//steps))
    else:
        g_range = [start[1] for _ in range(steps)]
    if (end[2]-start[2])//steps != 0:
        b_range = list(range(start[2], end[2], (end[2]-start[2])//steps))
    else:
        b_range = [start[2] for _ in range(steps)]
    return r_range, g_range, b_range

def rotaryDeal():
    global flag
    global Last_DT_Status
    global Current_DT_Status
    global globalCounter
    global servo_Counter
    global preview_color
    global colors
    Last_DT_Status = GPIO.input(DT)
    while not GPIO.input(CLK) :
        Current_DT_Status = GPIO.input(DT)
        flag = 1
    if flag == 1:
        flag = 0
        if Last_DT_Status == 1 and Current_DT_Status == 0 and globalCounter > 0:
            #globalCounter = (globalCounter - 1)% num_colors
            globalCounter = globalCounter - 1
            r_range, g_range, b_range = colorChange(preview_color, colors[globalCounter], 10)
            for r, g, b in zip(r_range, g_range, b_range):
                PWM(r,g,b)
            preview_color = colors[globalCounter]
            print(preview_color)
        if Last_DT_Status == 0 and Current_DT_Status == 1 and servo_Counter < 36:
            #globalCounter = (globalCounter + 1)% num_colors
            globalCounter = globalCounter + 1
            r_range, g_range, b_range = colorChange(preview_color, colors[globalCounter], 10)
            for r, g, b in zip(r_range, g_range, b_range):
                PWM(r,g,b)
            preview_color = colors[globalCounter]
            PWM(preview_color[0], preview_color[1], preview_color[2])
            print(preview_color)
        #servo
        if Last_DT_Status == 1 and Current_DT_Status == 0 and servo_Counter > 0 :#clock wise
            servo_Counter = servo_Counter - 1
        if Last_DT_Status == 0 and Current_DT_Status == 1 and servo_Counter < 36 :#reverse clock wise
            servo_Counter = servo_Counter + 1
            
def btnISR(channel):
    global globalCounter
    global preview_color
    print('button click')
    print(preview_color)
    globalCounter = 0
    preview_color = colors[0]
    PWM(preview_color[0], preview_color[1], preview_color[2])

def angle_to_duty_cycle(angle=0):
    duty_cycle = int((500*pwm_f)+(1900*pwm_f*angle / 180))
    return duty_cycle

def servo_move():
    global servo_Counter
    angle = 5 * servo_Counter #+ 90
    if angle == 0:
        angle+=3
    if angle == 180:
        angle-=3 
    dc = angle_to_duty_cycle(angle)
    pi.hardware_PWM(fan_angle_control,pwm_f,dc)
    pi.hardware_PWM(servo_control,pwm_f,dc)
    print('angle = {: >3}, work cycle={:.2f}'.format(angle,dc))
    

def fan_move():
    global fan_Counter
    angle = 5 * servo_Counter
    dc = angle_to_duty_cycle(angle)
    pi.hardware_PWM(fan_angle_control,pwm_f,dc)
    #pi.hardware_PWM(servo_control,pwm_f,dc)
    print('angle = {: >3}, work cycle={:.2f}'.format(angle,dc))

def loop():
    global globalCounter
    global servo_Counter
    tmp_global = 0
    tmp_servo = 0
    tmp_fan = 0
    #GPIO.add_event_detect(SW, GPIO.FALLING, callback=btnISR, bouncetime=1000)
    while True:
        rotaryDeal()
        if tmp_global != globalCounter:
            print('globalCounter = %d' % globalCounter)
        if tmp_servo != servo_Counter:
            print('servo_Counter = %d' % servo_Counter)
            servo_move()
        if tmp_fan != fan_Counter:
            print('fan_Counter = %d' % fan_Counter)
            fan_move()
        if tmp_global != globalCounter or tmp_servo != servo_Counter or tmp_fan != fan_Counter:
            try:
                requests.post(url+"/post_json", json={"globalCounter":globalCounter, "angle": 5 * servo_Counter}, timeout = 0.1)
            except Exception as e:
                print(e)
                print("Server post error")
            tmp_global = globalCounter
            tmp_servo = servo_Counter
            tmp_fan = fan_Counter
        if globalCounter == 36:
            Is_blueTear_end = False
            while True:
                try:
                    result = requests.get(url+"/get_end")
                    if str(result.content) == "b\'True\'":
                        print(type(result.content))
                        break
                except Exception as e:
                    print(e)
                    print("Server get error")
                else:
                    time.sleep(1)
            for angle in range(180,-1,-15):
                dc = angle_to_duty_cycle(angle)
                #pwm.ChangeDutyCycle(dc)
                pi.hardware_PWM(servo_control,pwm_f,dc)
                print(angle)
            tmp_global = 0
            tmp_servo = 0
            tmp_fan = 0
            globalCounter = 0
            servo_Counter = 0
            tmp_fan = 0
            try:
                requests.post(url+"/post_json", json={"globalCounter":globalCounter, "angle": 5 * servo_Counter}, timeout = 0.1)
            except:
                print("Server post error")

if __name__ == '__main__':    
    setup()
    pwm_r, pwm_g, pwm_b = setupPWM(2000, 100)
    colorFile_path = "color.txt"
    GPIO.output(sw, GPIO.HIGH)
    GPIO.output(R, GPIO.HIGH)
    GPIO.output(G, GPIO.HIGH)
    GPIO.output(B, GPIO.HIGH)
    #pwm = GPIO.PWM(servo_control,pwm_f)
    #pwm.start(0)
    with open(colorFile_path, 'r') as fout:
        for line in fout:
            colors.append(list(map(int, line.strip('\n').split(' '))))
    preview_color = colors[0]
    PWM(preview_color[0], preview_color[1], preview_color[2])
    num_colors = len(colors)
    try:
        loop()
    except KeyboardInterrupt:
        close()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          