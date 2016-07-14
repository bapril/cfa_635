"""
    Single LED control
"""
import sys
import subprocess
from threading import Thread
import shlex
import re

ON_POSIX = 'posix' in sys.builtin_module_names

class LED(object):
    def __init__(self, led, cfa, config):
        self.led = led - 1
        self.config = config
        self.cfa = cfa
        self.red = 0
        self.green = 0
        self.cfa.set_led(self.led, self.green, self.red)
        args = shlex.split(self.config['command'])
        self.process = subprocess.Popen(args, bufsize=1, stdout=subprocess.PIPE, close_fds=ON_POSIX)
        self.queue = None
        self.last_queue = None
        self.queue_thread = Thread(target=self.queue_input)
        self.queue_thread.daemon = True
        self.queue_thread.start()

    def queue_input(self):
        while self.process.poll() is None:
            line = self.process.stdout.readline()
            out = line.rstrip()
            if out != '':
                self.queue = out

    def update(self):
        if self.queue != self.last_queue:
            if self.queue == "OFF":
                self.cfa.set_led(self.led,0,0)
            elif self.queue == "RED":
                self.cfa.set_led(self.led,0,100)
            elif self.queue == "GREEN":
                self.cfa.set_led(self.led,100,0)
            elif self.queue == "YELLOW":
                self.cfa.set_led(self.led,50,100)
            elif self.queue == "ORANGE":
                self.cfa.set_led(self.led,100,100)
            else:
                args = re.findall('^(\d+):(\d+)$',self.queue)
                for ar in args:
                    self.cfa.set_led(self.led,int(ar[0]),int(ar[1]))
            self.last_queue = self.queue
