import Movement_Controller
import RepeatingTimer
from adafruit_pca9685 import PCA9685
import busio
from board import SCL, SDA

class Bot:
    __movement_controller = None
    __Update_Timer = None
    __i2c = None
    __pca = None
    __freq = 60

    def __init__(self):
        self.__i2c = busio.I2C(SCL, SDA)
        self.__pca = PCA9685(self.__i2c)
        self.__pca.frequency = self.__freq

    def Init_Movement_Device_As_Tracked(self):
        self.__movement_controller = Movement_Controller.Movement_Controller_Tracked(self.__pca)
        self.Set_Update_Interval(10)

    def Init_Movement_Device_As_Car(self):
        self.__movement_controller = Movement_Controller.Movement_Controller_Car(self.__pca)
        self.Set_Update_Interval(10)

    def Init_Movement_Device_As_Rover(self):
        self.__movement_controller = Movement_Controller.Movement_Controller_Rover(self.__pca)
        self.Set_Update_Interval(10)

    def Set_Update_Interval(self, interval):
        if (self.__Update_Timer != None):
            self.__Update_Timer.Stop()
        else:
            self.__Update_Timer = RepeatingTimer(interval, self._Update_Timer_Callback)
            self.__Update_Timer.Start()
    
    def _Update_Timer_Callback(self):
        #Recursively call the update functions of the movement controller and it's childeren.
        if (self.__movement_controller != None):
            self.__movement_controller.Update()
