"""FezHat 1.1 tools."""

import smbus
from RPi import GPIO


class Pins(object):
    """Store the address of the sensors."""

    SWITCH_LEFT = 18
    SWITCH_RIGHT = 22

    ANALOG_1 = 1
    ANALOG_2 = 2
    ANALOG_3 = 3
    ANALOG_6 = 6
    ANALOG_7 = 7

    LED = 24

class Fezhat(object):
    """Access to most sensors on the Fez Hat board."""

    def __init__(self, bus_id, address):
        """Access the bus on the board."""
        self._bus_id = bus_id
        self._address = address

        self._bus = smbus.SMBus(bus_id)

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(Pins.LED, GPIO.OUT)
        GPIO.setup(Pins.SWITCH_LEFT, GPIO.IN)
        GPIO.setup(Pins.SWITCH_RIGHT, GPIO.IN)

    def read(self, channel):
        """Read data on the channel."""
        chn_adr = 0b10000100 | ((channel / 2) if (channel % 2 == 0) else ((channel / 2) + 4)) << 4
        self._bus.write_byte(self._address, chn_adr)
        return self._bus.read_byte(self._address)

    @property
    def temperature(self):
        """Get temperature in Celsius."""
        return (((3300 / 255) * self.read(4)) - 400) / 19.5

    @property
    def light(self):
        """Get light sensor value 0.0-1.0."""
        return self.read(5) / 255.0

    @property
    def buttons(self):
        """Check which button is pressed."""
        switch_0 = GPIO.input(Pins.SWITCH_LEFT) == GPIO.LOW
        switch_1 = GPIO.input(Pins.SWITCH_RIGHT) == GPIO.LOW
        if switch_0 and switch_1:
            return 3
        elif switch_0:
            return 1
        elif switch_1:
            return 2
        elif not switch_0 and not switch_1:
            return 0
        else:
            raise Exception('Something went wrong with the buttons.')

    def led(self, state):
        """Change the state of the LED."""
        if not state in (0, 1):
            raise Exception('LED can only be set to 1 or 0.')
        if state == 1:
            GPIO.output(Pins.LED, GPIO.HIGH)
        else:
            GPIO.output(Pins.LED, GPIO.LOW)

