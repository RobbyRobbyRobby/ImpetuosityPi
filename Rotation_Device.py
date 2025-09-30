class Rotation_Device_Config:
    rotation_reversed = False #automaticaly reverse ann requested values
    rotation_max = 90
    rotation_home = 0
    rotation_min = -90
    rotation_current = 0
    pca9685 = None
    control_pin_index = -1
    position_change_degrees_per_second = -1 #negative = instant change
    
    # Constructor
    def __init__(self, pca, pin):
        if (pca == None or pin < 0):
            raise Exception("Invalid arguments. You need a PCA9685 device and control pin index.")
        else:
            self.pca9685 = pca
            self.control_pin_index = pin

class Rotation_Device:
    _rotation_reversed = False #automaticaly reverse ann requested values
    _rotation_current = 0
    _rotation_max = 0
    _rotation_home = 0
    _rotation_min = 0

    # Constructor
    def __init__(self, config):
        if (config != None):
            conf = Rotation_Device_Config(config)
        if (conf != None):
            self._rotation_reversed = conf.rotation_reversed
            self._rotation_current = conf.rotation_current
            self._rotation_max = conf.rotation_max
            self._rotation_home = conf.rotation_home
            self._rotation_min = conf.rotation_min
            self.Go_Home()

    # Destructor
    def __del__(self):
        pass

    def Set_Position(self, value):
        pass

    def Go_Home(self):
        self.Set_Position(self._rotation_home)
    
