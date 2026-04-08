class Propulsion_Device_Config:
    power_reversed = False  #automaticaly reverse ann requested values
    power_max = 100
    power_min = 0
    power_current = 0
    power_change_percent_per_second = -1 #negative = instant change
    pin_forward = -1
    pin_backward = -1
    pin_enable = -1

    # Constructor
    def __init__(self):
        pass

    # Constructor
    def __init__(self, pin_forward = 0, pin_backward = 0, pin_enable = 0, power_reversed = None, power_max = None, power_min = None, power_current = None, power_change_percent_per_second = None):
        if (pin_forward != None):
            self.pin_forward = pin_forward
        if (pin_backward != None):
            self.pin_backward = pin_backward
        if (pin_enable != None):
            self.pin_enable = pin_enable
        if (power_reversed != None):
            self.power_reversed = power_reversed
        if (power_max != None):
            self.power_max = power_max
        if (power_min != None):
            self.power_min = power_min
        if (power_current != None):
            self.power_current = power_current
        if (power_change_percent_per_second != None):
            self.power_change_percent_per_second = power_change_percent_per_second

import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from enum import Enum
import RPi.GPIO as GPIO
import math

class Propulsion_Device:
    _power_reversed = False  #automaticaly reverse ann requested values
    _power_max = 0
    _power_min = 0
    _power_current = 0
    _power_change_percent_per_second = -1 #negative = instant change
    _pin_forward = -1
    _pin_backward = -1
    _pin_enable = -1
    __PWMChannel = None
    __PWM_Frequency = 500

    # Constructor
    def __init__(self, config):
        #if (config != None):
            #print("Propulsion device created with config:",)
            #conf = config
        #else:
            #config = Propulsion_Device_Config()
            #print("Propulsion device created blank:", config)

        if (config != None):
            self._power_reversed = config.power_reversed
            self._power_max = config.power_max
            self._power_min = config.power_min
            self._power_current = config.power_current
            self._pin_forward = config.pin_forward
            self._pin_backward = config.pin_backward
            self._pin_enable = config.pin_enable
            self.Create_Motor_PWM_Channel()
            self.Set_Power(self._power_min)

    def Create_Motor_PWM_Channel(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin_forward, GPIO.OUT)
        print(self._pin_forward)
        GPIO.setup(self._pin_backward, GPIO.OUT)
        GPIO.setup(self._pin_enable, GPIO.OUT)
        GPIO.output(self._pin_forward, GPIO.LOW)
        GPIO.output(self._pin_backward, GPIO.LOW)
        self.__PWMChannel = GPIO.PWM(self._pin_enable, self.__PWM_Frequency)
        self.__PWMChannel.start(0)

    # Destructor
    def __del__(self):
        pass

    def Set_Power(self, value):
        #pass
        GPIO.output(self._pin_forward, GPIO.LOW)
        GPIO.output(self._pin_backward, GPIO.LOW)
        self.__PWMChannel.start(0)

        if (value > 1):
            GPIO.output(self._pin_forward, GPIO.HIGH)
        elif (value < -1):
            GPIO.output(self._pin_backward, GPIO.HIGH)
        else:
            exit

        self.__PWMChannel.start(max(math.fabs(value),100))
