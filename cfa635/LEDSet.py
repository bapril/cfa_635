"""
LED Management Module
"""
from cfa635.LED import LED
import sys

class LEDSet(object):
    l1 = None
    l2 = None
    l3 = None
    l4 = None
    def __init__(self, cfa, config):
        self.config = config['led_config']
        self.cfa = cfa
        if self.config['led1']:
            self.l1 = LED(1,self.cfa,self.config['led1'])
        if self.config['led2']:
            self.l2 = LED(2,self.cfa,self.config['led2'])
        if self.config['led3']:
            self.l3 = LED(3,self.cfa,self.config['led3'])
        if self.config['led4']:
            self.l4 = LED(4,self.cfa,self.config['led4'])

    def update(self):
        if self.l1 != None:
            self.l1.update()
        if self.l2 != None:
            self.l2.update()
        if self.l3 != None:
            self.l3.update()
        if self.l4 != None:
            self.l4.update()
