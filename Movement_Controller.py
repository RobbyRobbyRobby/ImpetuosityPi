import Movement_Device
from adafruit_pca9685 import PCA9685

class Movement_Controller:
    def __init__(self, pca9285):
        pass

    def Move(self, power, angle): # move at the requested power, turning at the requested angle (offset from 0 = straight ahead)
        pass

    def Rotate_For(self, power, seconds): # change direction without moving, to the requested angle offset from current direction
        pass

    def Adjust_Power_For_Pan(self):
        pass

    def Update(self):
        pass

    def _Set_Power(self, left, right):
        pass

# ===================================================
# ===================================================

# Like a 2wd or 4wd car with solid axels.  
# Can utilise / output
#   1 power value sent to all wheels/tracks, 
#   1 pan angle for steering
class Movement_Controller_Car(Movement_Controller):
    __movement_device_centre = None

    def __init__(self, pca9285):
        self.__movement_device_centre = Movement_Device(None, None, None)

    # move at the requested power, turning at the requested angle (offset from 0 = straight ahead)
    def Move(self, power, angle): 
        self._Set_Power(power, power)

    # change direction without moving, to the requested angle offset from current direction
    def Rotate_For(self, power, seconds): # change direction without moving, to the requested angle offset from current direction
        # Not supported in this configuration
        pass

    def Adjust_Power_For_Pan(self):
        pass

    def Update(self):
        self.__movement_device_centre.Update()

    def _Set_Power(self, left, right):
        self.__movement_device_centre.Set_Propulsion_Power((left + right) / 2)

# ===================================================
# ===================================================

# Tanks and vehicles that steer by varying propulsion power.  
# Can utilise / output
#   2 power values; one left, one right.
#   0 pan values.
class Movement_Controller_Tracked(Movement_Controller): 
    __movement_device_left = None
    __movement_device_right = None

    def __init__(self, pca9285):
        self.__movement_device_left = Movement_Device(None, None, None) 
        self.__movement_device_right = Movement_Device(None, None, None)

    # move at the requested power, turning at the requested angle (offset from 0 = straight ahead)
    def Move(self, power, angle): # move at the requested power, turning at the requested angle (offset from 0 = straight ahead)
        self._Set_Power(power, power)

    # change direction without moving, to the requested angle offset from current direction
    def Rotate_For(self, power, seconds): 
        pass

    def Adjust_Power_For_Pan(self):
        pass

    def Update(self):
        self.__movement_device_left.Update()
        self.__movement_device_right.Update()

    def _Set_Power(self, left, right):
        self.__movement_device_left.Set_Propulsion_Power(left)
        self.__movement_device_right.Set_Propulsion_Power(right)
    
# ===================================================
# ===================================================

# Left/Right power, 4 panning wheels.  Includes rovers with 4 and 6 wheels with corner panning.
# Can utilise / output
#   2 power values; one left, one right.
#   4 independant steering angles.
class Movement_Controller_Rover(Movement_Controller): 
    __movement_device_left = None
    __movement_device_right = None

    def __init__(self, pca9285):
        self.__movement_device_left = Movement_Device(Propulsion_Config() , None, None) 
        self.__movement_device_right = Movement_Device(None, None, None)

    # move at the requested power, turning at the requested angle (offset from 0 = straight ahead)
    def Move(self, power, angle): 
        # Pan corner wheels, power corner wheels.  Adjust power for each wheel depending on the angle requested.
        # Pan is set to value requested.
        # power and angle can be set in parallel.
        # Dont stop first.        
        self._Set_Power(power, power)

    # change direction without moving, to the requested angle offset from current direction
    def Rotate_For(self, power, seconds): 
        #Note, Halt first, then complete wheel rotation, then apply power.
        pass

    def Adjust_Power_For_Pan(self):
        pass

    def Update(self):
        self.__movement_device_left.Update()
        self.__movement_device_right.Update()

    def _Set_Power(self, left, right):
        self.__movement_device_left.Set_Propulsion_Power(left)
        self.__movement_device_right.Set_Propulsion_Power(right)
