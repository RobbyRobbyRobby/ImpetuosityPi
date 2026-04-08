import Movement_Controller
import RepeatingTimer
from adafruit_pca9685 import PCA9685
import busio
from board import SCL, SDA

class Bot_Master_Controller:
    __movement_controller = None
    __Update_Timer = None
    __i2c = None
    __pca = None
    __freq = 50

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
        self.Set_Update_Interval()

    def Set_Update_Interval(self, interval = 0.1):
        if (self.__Update_Timer != None):
            self.__Update_Timer.stop()
        else:
            print("Starting Update 'Heartbeat' at interval of:", interval)
            self.__Update_Timer = RepeatingTimer.RepeatingTimer(interval, self._Update_Timer_Callback)
            self.__Update_Timer.start()
            print("Heartbeat Started")

    #Recursively call the update functions of the movement controller and it's childeren.
    def _Update_Timer_Callback(self):
        #print("update")
        if (self.__movement_controller != None):
            self.__movement_controller.Update()

    def Move(self, power, angle):
        self.__movement_controller.Move(power, angle)

    def Rotate_To(self, newAngle):
        self.__movement_controller.Rotate_To(newAngle)
