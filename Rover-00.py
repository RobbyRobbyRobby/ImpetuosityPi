import Bot_Master_Controller
import time

bot = Bot_Master_Controller.Bot_Master_Controller()
bot.Init_Movement_Device_As_Rover()
testing_power_on = True

while True:
    time.sleep(1)
    if (testing_power_on == True):
        print("rotate/move")
        bot.Rotate_To(0) #centre the drive servos
        #bot.Move(100,0)
        time.sleep(1)
        testing_power_on = False
        print("stop")
        bot.Move(0,0)
