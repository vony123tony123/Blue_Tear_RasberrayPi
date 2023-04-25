import RPi.GPIO as GPIO
import time
import pigpio
import requests

sw = 17#11
R = 22#15
G = 27#13
B = 23#16

CLK = 14#8
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

url = "http://169.254.84.78:6200"

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
    pi.hardware_PWM(servo_control,pwm_f,angle_to_duty_cycle(177))
    pi.hardware_PWM(fan_angle_control,pwm_f,angle_to_duty_cycle(177))
    
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


def angle_to_duty_cycle(angle=0):
    duty_cycle = int((500*pwm_f)+(1900*pwm_f*angle / 180))
    return duty_cycle

def led_change(counter):
    global preview_color
    global colors
    r_range, g_range, b_range = colorChange(preview_color, colors[counter], 10)
    for r, g, b in zip(r_range, g_range, b_range):
        PWM(r,g,b)
        time.sleep(0.01)
    preview_color = colors[counter]
    PWM(preview_color[0], preview_color[1], preview_color[2])
    print(preview_color)

def servo_move(counter):
    angle =180 - 5 * counter #+ 90
    if angle == 0:
        angle+=3
    if angle == 180:
        angle-=5 
    dc = angle_to_duty_cycle(angle)
    pi.hardware_PWM(fan_angle_control,pwm_f,dc)
    pi.hardware_PWM(servo_control,pwm_f,dc)
    print('sun angle = {: >3}, work cycle={:.2f}'.format(angle,dc))
    

def fan_move(counter):
    angle = 180 - (5 * counter)
    dc = angle_to_duty_cycle(angle)
    pi.hardware_PWM(fan_angle_control,pwm_f,dc)
    #pi.hardware_PWM(servo_control,pwm_f,dc)
    print('fan angle = {: >3}, work cycle={:.2f}'.format(angle,dc))

def loop():
    global preview_counter
    current_counter = 0
    preview_counter = 0
    reverse = False
    
    #GPIO.add_event_detect(SW, GPIO.FALLING, callback=btnISR, bouncetime=1000)
    while True:
        try:
            result = requests.get(url+"/get_end")
            message = str(result.content)
#             print(message)
            message = message[2:-1].split(',')
            reverse = message[0] == 'True'
            current_counter = int(message[1])
            if current_counter == 37:#??
                current_counter = 36
            print(reverse, current_counter)
        except Exception as e:
            print(e)
            print("Server get error")
            continue
        
#         if reverse == True:
#             for angle in range(0,181,15):
#                 dc = angle_to_duty_cycle(angle)
#                 #pwm.ChangeDutyCycle(dc)
#                 pi.hardware_PWM(servo_control,pwm_f,dc)
#                 time.sleep(1)
#                 print(angle)
#             current_counter = 0
#             prview_counter = 0
#             try:
#                 requests.post(url+"/post_json", json={"globalCounter": current_counter, "angle": 5 * current_counter}, timeout = 0.1)
#             except:
#                 print("Server post error")
#             continue
#                 
            
        if current_counter != preview_counter:
            print(current_counter)
            if reverse == False:
                led_change(current_counter)
            fan_move(current_counter)
            servo_move(current_counter)
            preview_counter = current_counter
            
            

if __name__ == '__main__':
    setup()
    pwm_r, pwm_g, pwm_b = setupPWM(2000, 100)
    colorFile_path = "/home/user/color5V_ver2.1.txt"
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