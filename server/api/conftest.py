import random
from time import sleep


class MetaDelaySerial(type):
    def __new__(cls, name, bases, attrs):
        for attr, value in attrs.items():
            if callable(value):
                attrs[attr] = cls.pre_call(value)
        return super().__new__(cls, name, bases, attrs)

    @staticmethod
    def pre_call(func):
        def wrapper(*args, **kwargs):
            sleep(0.3)
            return func(*args, **kwargs)

        return wrapper


class MockedPSU(metaclass=MetaDelaySerial):
    def __init__(self):
        self.__is_on = False
        self.__voltage = 0
        self.__current = 0

    def get_model(self):
        return "HDP1160V4S"

    def get_on_off_status(self):
        return self.__is_on

    def turn_on(self):
        self.__is_on = True

    def turn_off(self):
        self.__is_on = False

    def set_output_voltage(self, voltage):
        self.__voltage = voltage

    def set_output_current(self, current):
        self.__current = current

    def get_active_voltage(self):
        if not self.__is_on:
            return 0
        return self.__voltage + self.__voltage * 0.002 * (2 * random.random() - 1)

    def get_active_current(self):
        if not self.__is_on:
            return 0
        return self.__current + self.__current * 0.002 * (2 * random.random() - 1)

    def get_voltage_limit(self):
        return self.__voltage

    def get_current_limit(self):
        return self.__current
