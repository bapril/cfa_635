"""
LED Management Module
"""
from cfa635.LED import LED

class LEDSet(object):
    """
    Set of 4 LEDs as present on the CFA635
    """
    led1 = None
    led2 = None
    led3 = None
    led4 = None
    def __init__(self, cfa, config):
        self.config = config['led_config']
        self.cfa = cfa
        if self.config['led1']:
            self.led1 = LED(1, self.cfa, self.config['led1'])
        if self.config['led2']:
            self.led2 = LED(2, self.cfa, self.config['led2'])
        if self.config['led3']:
            self.led3 = LED(3, self.cfa, self.config['led3'])
        if self.config['led4']:
            self.led4 = LED(4, self.cfa, self.config['led4'])

    def update(self):
        """
        Pass the update on to each configured LED
        """
        if self.led1 != None:
            self.led1.update()
        if self.led2 != None:
            self.led2.update()
        if self.led3 != None:
            self.led3.update()
        if self.led4 != None:
            self.led4.update()
