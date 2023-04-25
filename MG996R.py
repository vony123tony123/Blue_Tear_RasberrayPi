# Servo_test32 tlfong01 2019may12hkt1506 ***
# Raspbian stretch 2019apr08, Python 3.5.3

import RPi.GPIO as GPIO
from time import sleep

# *** GPIO Housekeeping Functions ***

def setupGpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    return

def cleanupGpio():
    GPIO.cleanup()
    return

# *** GPIO Input/Output Mode Setup and High/Low Level Output ***

def setGpioPinLowLevel(gpioPinNum):
    lowLevel = 0
    GPIO.output(gpioPinNum, lowLevel)
    return

def setGpioPinHighLevel(gpioPinNum):
    highLevel = 1
    GPIO.output(gpioPinNum, highLevel)
    return

def setGpioPinOutputMode(gpioPinNum):
    GPIO.setup(gpioPinNum, GPIO.OUT)
    setGpioPinLowLevel(gpioPinNum)
    return

# *** GPIO PWM Mode Setup and PWM Output ***

def setGpioPinPwmMode(gpioPinNum, frequency):
    pwmPinObject = GPIO.PWM(gpioPinNum, frequency)
    return pwmPinObject

def pwmPinChangeFrequency(pwmPinObject, frequency):
    pwmPinObject.ChangeFrequency(frequency)
    return

def pwmPinChangeDutyCycle(pwmPinObject, dutyCycle):
    pwmPinObject.ChangeDutyCycle(dutyCycle)
    return

def pwmPinStart(pwmPinObject):
    initDutyCycle = 50
    pwmPinObject.start(initDutyCycle)
    return

def pwmPinStop(pwmPinObject):
    pwmPinObject.stop()
    return

# *** Test Functions ***

def setHighLevelGpioPin18():
    print('  Begin setHighLevelGpioPin18, ...')
    gpioPinNum   = 18
    sleepSeconds =  2    
    setupGpio()
    setGpioPinOutputMode(gpioPinNum)
    setGpioPinHighLevel(gpioPinNum)
    sleep(sleepSeconds)
    cleanupGpio()
    print('  End setHighLevelGpioPin18, ...\r\n')
    return

def setPwmModeGpioPin18():
    print('  Begin setPwmModeGpioPin18, ...')

    gpioPinNum   =   18
    sleepSeconds =   10
    frequency    = 1000
    dutyCycle    =   50

    setupGpio()
    setGpioPinOutputMode(gpioPinNum)

    pwmPinObject = setGpioPinPwmMode(gpioPinNum, frequency)
    pwmPinStart(pwmPinObject)
    pwmPinChangeFrequency(pwmPinObject, frequency)
    pwmPinChangeDutyCycle(pwmPinObject, dutyCycle)
    sleep(sleepSeconds)
    pwmPinObject.stop()
    cleanupGpio()   

    print('  End   setPwmModeGpioPin18, ...\r\n')

    return

# *** Main ***

print('Begin testing, ...\r\n')
setHighLevelGpioPin18()
setPwmModeGpioPin18()
print('End   testing.')

# *** End of program ***

'''
Sample Output - 2019may12hkt1319
>>> 
 RESTART: /home/pi/Python Programs/Python_Programs/test1198/servo_test31_2019may1201.py 
Begin testing, ...

  Begin setHighLevelGpioPin18, ...
  End setHighLevelGpioPin18, ...

  Begin setPwmModeGpioPin18, ...
  End   setPwmModeGpioPin18, ...

End   testing.
>>> 

>>> 


'''
