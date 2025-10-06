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
    def __init__(self):
        pass

    # Constructor
    def __init__(self, rotation_reversed, rotation_max, rotation_home, rotation_min, rotation_current, pca9685, control_pin_index, position_change_degrees_per_second):
        if (rotation_reversed != None):
            self.rotation_reversed = rotation_reversed
        if (rotation_max != None):
            self.rotation_max = rotation_max
        if (rotation_home != None):
            self.rotation_home = rotation_home
        if (rotation_min != None):
            self.rotation_min = rotation_min
        if (pca9685 != None):
            self.pca9685 = pca9685
        if (control_pin_index != None):
            self.control_pin_index = control_pin_index
        if (rotation_current != None):
            self.rotation_current = rotation_current
        if (position_change_degrees_per_second != None):
            self.position_change_degrees_per_second = position_change_degrees_per_second

    # Constructor
    def __init__(self, pca9685, control_pin_index):
        if (pca9685 == None or control_pin_index < 0):
            raise Exception("Invalid arguments. You need a PCA9685 device and control pin index.")
        else:
            if (pca9685 != None):
                self.pca9685 = pca9685
            if (control_pin_index != None):
                self.control_pin_index = control_pin_index

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
    
