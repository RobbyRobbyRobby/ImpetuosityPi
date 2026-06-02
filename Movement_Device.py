import Propulsion_Device
import Rotation_Device

class Movement_Device:

    def __init__(self):
        # Default Constructor
        pass

    # Constructor
    def __init__(self, propulsion_config, pan_config, tilt_config):
        print("Movement Device constructor.")
        self._Init_Propulsion(propulsion_config)
        self._Init_Pan(pan_config)
        self._Init_Tilt(tilt_config)

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
            self.__propulsion = Propulsion_Device.Propulsion_Device(self.__propulsion_config)
        else:
            print("Skipping init of propulsion device; no config provided.")

    def _Get_Propulsion_Enabled(self):
        return self.__propulsion != None

#    def _Set_Propulsion_Enabled(self, value):
#        self.__propulsion = value

    def _Update_Propulsion(self):
        pass

    #=================================================
    # Pan
    #=================================================

    __pan_config = None
    __pan = None

    def _Init_Pan(self, config):
        if (config == None):
            print("no pan config passed")
        else:
            print("Init pan on movement device", config._index)
            self.__pan_config = config
            if (self.__pan_config != None):
                print("pan config available")
                self.__pan = Rotation_Device.Rotation_Device(self.__pan_config)

    def _Get_Pan_Enabled(self):
        return self.__pan != None

    def _Update_Pan(self):
        pass

    def Pan_To(newAngle):
        print("Pan Requested")
        self.__pan.Set_Position(newAngle)
        pass

    #=================================================
    # Tilt
    #=================================================

    __tilt_config = None
    __tilt = None

    def _Init_Tilt(self, config):
        self.__tilt_config = config
        if (self.__tilt_config != None):
            self.__tilt = Rotation_Device.Rotation_Device(self.__tilt_config)

    def _Get_Tilt_Enabled(self):
        return self.__tilt == None

    def _Update_Tilt(self):
        pass

    #=================================================
    # Properties and public bits
    #=================================================
    Propulsion_Enabled = property(_Get_Propulsion_Enabled, None, None, "")

    def Request_Propulsion_Power(self, value):
        if self.Propulsion_Enabled:
            self.__propulsion.Set_Power(value)
            print("Propulsion power set to ", value)
        else:
            print("Error setting propulsion power; enabled == False")

    Pan_Enabled = property(_Get_Pan_Enabled, None, None, "")

    def Request_Pan_Position(self, value):
        if self.Pan_Enabled:
            self.__pan.Set_Position(value)
        else:
            print("Pan not enabled")

    Tilt_Enabled = property(_Get_Tilt_Enabled)

    def Request_Tilt_Position(self, value):
        if self.__tilt_enabled:
            self.__tilt.Set_Position(value)

    def Update(self):
        self._Update_Propulsion()
        self._Update_Pan()
        self._Update_Tilt()
