class Propulsion_Device_Config:
    power_reversed = False  #automaticaly reverse ann requested values
    power_max = 100
    power_min = 0
    power_current = 0
    power_change_percent_per_second = -1 #negative = instant change

class Propulsion_Device:
    _power_reversed = False  #automaticaly reverse ann requested values
    _power_max = 0
    _power_min = 0
    _power_current = 0

    # Constructor
    def __init__(self, config):
        if (config != None):
            conf = Propulsion_Device_Config(config)
        if (conf != None):
            self._power_reversed = conf.power_reversed
            self._power_max = conf.power_max
            self._power_min = conf.power_min
            self._power_current = conf.power_current
            self.Set_Power(self._power_min)

    # Destructor
    def __del__(self):
        pass

    def Set_Power(self, value):
        pass