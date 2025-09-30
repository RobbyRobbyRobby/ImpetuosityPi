import Movement_Controller
import timer

class Bot:

    __movement_controller = None
    __Update_Timer = None

    def __init__(self):
        self.Set_Update_Interval(10)

    def Init_Movement_Device_As_Tracked(self):
        self.__movement_controller = Movement_Controller.Movement_Controller_Tracked()

    def Init_Movement_Device_As_Car(self):
        self.__movement_controller = Movement_Controller.Movement_Controller_Car()

    def Init_Movement_Device_As_Rover(self):
        self.__movement_controller = Movement_Controller.Movement_Controller_Rover()

    def Set_Update_Interval(self, interval):
        if (self.__Update_Timer != None):
            self.__Update_Timer.Set_Interval(interval)
        else:
            self.__Update_Timer = timer.Repeating_Timer(interval)
            self.__Update_Timer.Start()
        self.__Update_Timer.Set_Callback(self._Update_Timer_Callback)
    
    def _Update_Timer_Callback(self):
        if (self.__movement_controller != None):
            self.__movement_controller.Update()
