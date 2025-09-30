import Propulsion_Device
import Rotation_Device

class Movement_Device:

    # Constructor
    def __init__(self, propulsion_config, pan_config, tilt_config):
        self._Set_Tilt_Config(propulsion_config)
        self._Set_Propulsion_Config(pan_config)
        self._Set_Propulsion_Config(tilt_config)

    # Destructor
    def __del__(self):
        pass

    #=================================================
    # Worker methods
    #=================================================



    #=================================================
    # Propulsion
    #=================================================

    __propulsion_config = None
    __propulsion = None

    # set the config and load device if config exists
    def _Init_Propulsion(self, config):
        self.__propulsion_config = config
        if (self.__propulsion_config != None):
            self.__propulsion = Propulsion_Device(self.__propulsion_config)

    def _Get_Propulsion_Enabled(self):
        return self.__propulsion == None

    #=================================================
    # Pan
    #=================================================

    __pan_config = None
    __pan = None

    def _Init_Pan(self, config):
        self.__pan_config = config
        if (self.__pan_config != None):
            self.__pan = Rotation_Device(self.__pan_config)

    def _Get_Pan_Enabled(self):
        return self.__pan == None

    #=================================================
    # Tilt
    #=================================================

    __tilt_config = None
    __tilt = None

    def _Init_Tilt(self, config):
        self.__tilt_config = config
        if (self.__tilt_config != None):
            self.__tilt = Rotation_Device(self.__tilt_config)

    def _Get_Tilt_Enabled(self):
        return self.__tilt == None
    
    #=================================================
    # Properties and public bits
    #=================================================
    
    Propulsion_Enabled = property(_Get_Propulsion_Enabled)    

    def Request_Propulsion_Power(self, value):
        if self.__propulsion_enabled:
            self.__propulsion.Set_Power(value)


    Pan_Enabled = property(_Get_Pan_Enabled)

    def Request_Pan_Position(self, value):
        if self.__pan_enabled:
            self.__pan.Set_Position(value)


    Tilt_Enabled = property(_Get_Tilt_Enabled)

    def Request_Tilt_Position(self, value):
        if self.__tilt_enabled:
            self.__tilt.Set_Position(value)
    
    def Update(self):
        pass