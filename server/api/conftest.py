class MockedPSU:
    def __init__(self):
        self.__is_on = True
    def get_model(self):
        return "HDP1160V4S"
    def get_on_off_status(self):
        return self.__is_on
    def turn_on(self):
        self.__is_on = True
    def turn_off(self):
        self.__is_on = False
    def set_output_voltage(self, voltage):
        pass
    def set_output_current(self, current):
        pass
    def get_output_voltage(self):
        return 0
    def get_output_current(self):
        return 0

