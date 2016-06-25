"""
Module containing functions for every activity availiable in the CFA635 API
"""
from cfa635.API import API
import time

class Controller:
    """
    Class driving the LCD with easy to call functions
    """

    dev = None
    backlight_set = 0
    backlight_current = 0

    KEY_UP     = 0x01
    KEY_OK     = 0x02
    KEY_STOP   = 0x04
    KEY_LEFT   = 0x08
    KEY_RIGHT  = 0x10
    KEY_DOWN   = 0x20

    CURSOR_NO              = 0x00
    CURSOR_BLINK_BLOCK     = 0x01
    CURSOR_UNDER           = 0x02
    CURSOR_BLINK_UNDER     = 0x03
    CURSOR_INV_BLINK_UNDER = 0x04

    def __init__ (self, dev):
        self.dev = dev
        self.api = API(dev)
        return None

    def flush_key_input(self):
        """ Take input from keypad and ignore
        """
        self.api.read_keypad()

    def wait_for_input(self, timeout):
        """ Loops checking for input,
            Takes timeout
            returns True/False Did we get input.
        """
        while True:
            time.sleep(0.1)
            (now, _press, _release) = self.api.read_keypad()
            if ord(now) != 0:
                print "Key Pressed", ord(now)
                return True
            timeout -= 1
            if timeout < 1:
                return False

    def get_input(self, timeout):
        """ Timeout limited input request. Returns keycode currently pressed.
        """
        while True:
            time.sleep(0.1)
            (now, _press, _release) = self.api.read_keypad()
            if ord(now) != 0:
                print "Key Pressed", ord(now)
                return (True, ord(now))
            timeout -= 1
            if timeout < 1:
                return (False, None)

    def sleep_wait_for_input(self):
        """ Long slow wait for input.
            To be used after screen has gone to sleep.
        """
        while True:
            time.sleep(.25)
            (now, _press, _release) = self.api.read_keypad()
            if ord(now) != 0:
                print "Key Pressed", ord(now)
                return True

    def set_led (self, row, green, red):
        """ Set a LED
        """
        if red > 100 and green > 100:
            raise Exception("Maximum LED value is 100")
        if row > 3:
            raise Exception("Row number greater than 3")
        led = [[11, 12], [9, 10], [7, 8], [5, 6]]
        self.api.set_gpio(led[row][0], green)
        self.api.set_gpio(led[row][1], red)

    def go_to_sleep(self):
        """ decrease backlight to zero
        """
        self.backlight_set = self.backlight_current
        while(self.backlight_current > 0):
            self.api.set_backlight(self.backlight_current - 1)

    def wake_up(self):
        """ return backlight to previous level
        """
        while(self.backlight_current != self.backlight_set):
            self.api.set_backlight(self.backlight_current + 1)
