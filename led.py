import RPi.GPIO as GPIO
import time

sw = 11
R = 15
G = 13
B = 16


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(sw, GPIO.OUT)
    GPIO.setup(R, GPIO.OUT)
    GPIO.setup(G, GPIO.OUT)
    GPIO.setup(B, GPIO.OUT)
    
def setupPWM(freq, dc):
    pwm_r = GPIO.PWM(R, freq)
    pwm_b = GPIO.PWM(B, freq)
    pwm_g = GPIO.PWM(G, freq)
    pwm_r.start(dc)
    pwm_g.start(dc)
    pwm_b.start(dc)
    return pwm_r, pwm_g, pwm_b

def test():
    GPIO.output(sw, GPIO.HIGH)
    GPIO.output(R, GPIO.LOW)
    GPIO.output(G, GPIO.LOW)
    GPIO.output(B, GPIO.HIGH)
    while True:
        True
        
def testPWM():
    freq = 2000
    dc = 100
    GPIO.output(sw, GPIO.HIGH)
    GPIO.output(R, GPIO.HIGH)
    GPIO.output(G, GPIO.HIGH)
    GPIO.output(B, GPIO.HIGH)
    pwm = GPIO.PWM(B, freq)
    pwm.start(dc)
    freq = int(input("Enter frequency of PWM(1-2000)"))
    pwm.ChangeFrequency(freq)
    while True:
        dc = int(input("Enter duty cycle of PWM(1-100)"))
        pwm.ChangeDutyCycle(dc)
        
def PWM(R_value, G_value, B_value):
    #if R_value - 20 < 0:
    #    pwm_r.ChangeDutyCycle(0)
    #else:
    #    pwm_r.ChangeDutyCycle(R_value-20)
    #if G_value + 10 > 100:
    #    pwm_g.ChangeDutyCycle(100)
    #else:
    #    pwm_g.ChangeDutyCycle(G_value+10)
    #if B_value + 20 >100:
    #    pwm_b.ChangeDutyCycle(100)
    #else:
    #    pwm_b.ChangeDutyCycle(B_value+20)
    pwm_r.ChangeDutyCycle(R_value)
    pwm_g.ChangeDutyCycle(G_value)
    pwm_b.ChangeDutyCycle(B_value)
    time.sleep(0.1)
    
def close():
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

if __name__ == "__main__":
    
  freq = 2000
  dc = 100
  try:
      setup()
      #testPWM()
      
      pwm_r, pwm_g, pwm_b = setupPWM(freq, dc)
      colorFile_path = "/home/user/color5V_ver2.1.txt"
      GPIO.output(sw, GPIO.HIGH)
      GPIO.output(R, GPIO.HIGH)
      GPIO.output(G, GPIO.HIGH)
      GPIO.output(B, GPIO.HIGH)
#       with open(colorFile_path, 'r') as fout:
#           lines = fout.readlines()
#           start = lines.pop(0).strip().split(' ')
#           start = list(map(int, start))
#           for line in lines:
#               color = line.strip().split(' ')
#               end = list(map(int, color))
#               if abs(start[1]-end[1]) == 1 and (start[1]==100 or end[1]== 100):
#                   start = end
#                   print("skip")
#                   print(color)
#                   continue
#               print(color)
#               r_range, g_range, b_range = colorChange(start, end, 10)
#               for r, g, b in zip(r_range, g_range, b_range):
#                   PWM(r,g,b)
#                   time.sleep(0.01)
#               start = end
#       for g in range(100, 50, -5):
#           for b in range(100, 50, -5):
#               print(0,g,b)
#               PWM(0,g,b)
#               time.sleep(0.5)
      while True:
           PWM(40,95,100)
#       
  finally:
    close()
    