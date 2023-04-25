import RPi.GPIO as GPIO
import time
import pigpio

control = 18
pwm_f = 50
step = 5

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(control,GPIO.OUT)

#pwm = GPIO.PWM(control,pwm_f)
#pwm.start(0)
pi = pigpio.pi()
pi.set_mode(control,pigpio.OUTPUT)

def angle_to_duty_cycle(angle=0):
    duty_cycle = int((500*pwm_f)+(1900*pwm_f*angle / 180))
    return duty_cycle
def loop():
    try:
        print("Press ctrl c to Stop")
        #pi.hardware_PWM(control,pwm_f,20000)
        while True:
            for angle in range(0,181,step):
                dc = angle_to_duty_cycle(angle)
                #pwm.ChangeDutyCycle(dc)
                pi.hardware_PWM(control,pwm_f,dc)
                print('angle = {: >3}, work cycle={:.2f}'.format(angle,dc))
                time.sleep(0.5)
            for angle in range(180,-1,-step):
                dc = angle_to_duty_cycle(angle)
                #pwm.ChangeDutyCycle(dc)
                print('angle = {: >3}, work cycle={:.2f}'.format(angle,dc))
                time.sleep(0.5)
                pi.hardware_PWM(control,pwm_f,dc)
                #print(p(1))
            #pwm.ChangeDutyCycle(angle_to_duty_cycle(90))
    except KeyboardInterrupt:
        print("Close")
    finally:
        pi.stop()
        GPIO.cleanup()
if __name__ == '__main__':
    #loop()
    dc = angle_to_duty_cycle(3)
    pi.hardware_PWM(control,pwm_f,dc)
