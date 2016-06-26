"""
An object supporting a given line.
"""
import os
from cfa635.ByteString import ByteString
import math

class Line(object):
    """
    Generic line class that will display a line.
    """
    line = {}
    row = 0
    cfa = None

    def route(self):
        """
        Return the appropriate line object based on the config for this line.
        """
        if 'line_type' in self.line:
            if self.line['line_type'] == 'value_bar':
                return ValueBar(self.line)
            elif self.line['line_type'] == 'value_bar_contrast':
                return ValueBarContrast(self.line)
            elif self.line['line_type'] == 'value_bar_brightness':
                return ValueBarBrightness(self.line)
            elif self.line['line_type'] == 'cmd_line':
                return CmdLine(self.line)
        return self

    def render(self, row, cfa):
        """
        Render the line text
        """
        self.row = row
        self.cfa = cfa
        text = self.cfa_bs.pad(self.line['line_text'], 20)
        self.cfa.api.set_text(self.row, 0, text)

    def process_key(self, key, cfa):
        """
        Result is in the following tuple:
        {action_taken: bool, new_action:string}
        action_taken will be true if we did something and the parent is done.
        new_action is an action we are asking parent to take.
        """
        if key == cfa.KEY_UP:
            return (False, None)
        elif key == cfa.KEY_DOWN:
            return (False, None)
        elif key == cfa.KEY_LEFT or key == cfa.KEY_STOP:
            return (False, None)
        elif key == cfa.KEY_RIGHT or key == cfa.KEY_OK:
            if 'action' in self.line:
                return (True, self.line['action'])
            else:
                return (False, None)
        else:
            return (False, None)

    def __init__ (self, line):
        self.line = line
        self.row = 0
        self.cfa_bs = ByteString()
        return None

class CmdLine(Line):
    """
    This Line type uses the stdout of a command
    to generate the line text
    """
    def render(self, row, cfa):
        """
        Execute the command and render the line text
        """
        self.row = row
        self.cfa = cfa
        text = os.popen(self.line['line_cmd']).read().rstrip()
        text = self.cfa_bs.pad(text, 20)
        self.cfa.api.set_text(self.row, 0, text)

    def __init__ (self, line):
        super(CmdLine, self).__init__(line)
        return None

class ValueBar(Line):
    """
    A fader-style input field. with number and bargraph
    """

    value = 50
    row = 0
    max = 0
    min = 0
    inc = 0
    value = None
    state = 'select'

    def generate_bar(self, size):
        """
        Turn the current value into a graphical bar graph.
        """
        out = ""
        point_range = (self.max - self.min)
        points_per_col = math.ceil(point_range/size)/5
        value = self.value
        while(value >= (points_per_col * 5)):
            out += "#d214"
            value -= (points_per_col * 5)
        if value >= (points_per_col * 4):
            out += "#d215"
        elif value >= (points_per_col * 3):
            out += "#d216"
        elif value >= (points_per_col * 2):
            out += "#d217"
        elif value >= (points_per_col):
            out += "#d218"
        return out

    def render(self, row, cfa):
        """
        Render the line text
        """
        self.row = row
        self.cfa = cfa
        size = 18
        text = " " + self.cfa_bs.pad(str(self.value), 3) + " : "
        size = size - len(text)
        bar_string = self.generate_bar(size)
        text = self.cfa_bs.pad(text + bar_string, 20)
        self.cfa.api.set_text(self.row, 0, text)

    def increment(self, cfa):
        """
        User increased the value, update display
        """
        self.value += self.inc
        if self.value > self.max:
            self.value = self.max
        self.render(self.row, cfa)

    def decrement(self, cfa):
        """
        User decreased the value, update display
        """
        self.value -= self.inc
        if self.value < self.min:
            self.value = self.min
        self.render(self.row, cfa)

    def process_key(self, key, cfa):
        """
        Result is in the following tuple:
        {action_taken: bool, new_action:string}
        action_taken will be true if we did something and the parent is done.
        new_action is an action we are asking parent to take.
        """
        if self.state == 'select':
            if key == cfa.KEY_RIGHT or key == cfa.KEY_OK:
                cfa.api.set_cursor_style(cfa.CURSOR_INV_BLINK_UNDER)
                self.state = 'edit'
                return (True, None)
        elif self.state == 'edit':
            if key == cfa.KEY_UP or key == cfa.KEY_RIGHT:
                self.increment(cfa)
                return (True, None)
            elif key == cfa.KEY_LEFT or key == cfa.KEY_DOWN:
                self.decrement(cfa)
                return (True, None)
            elif key == cfa.KEY_STOP:
                self.get_value()
                self.state = 'select'
                cfa.api.set_cursor_style(cfa.CURSOR_NO)
                return (True, None)
            elif key == cfa.KEY_OK:
                self.set_value()
                self.state = 'select'
                cfa.api.set_cursor_style(cfa.CURSOR_NO)
                return (True, None)
        return (False, None)

    def get_value(self):
        """
        Get the value for this field from the defaults file.
        """
        self.value = int(os.popen(self.line['vbar_read']).read().rstrip())

    def set_value(self):
        """
        Set the value for this filed into the defaults file.
        """
        cmd = self.line['vbar_write']
        cmd = cmd.replace('%v', str(self.value))
        os.system(cmd)

    def __init__ (self, line):
        super(ValueBar, self).__init__(line)
        self.max = self.line['vbar_max']
        self.min = self.line['vbar_min']
        self.inc = self.line['vbar_inc']
        self.get_value()
        return None

class ValueBarContrast(ValueBar):
    """
    A valueBar module updated to manage contrast
    """

    def increment(self, cfa):
        """ Increment Contrast to the upper limit.
        and update the display.
        """
        self.value += self.inc
        if self.value > self.max:
            self.value = self.max
        cfa.api.set_contrast(self.value)
        self.render(self.row, cfa)

    def decrement(self, cfa):
        """ deccrement Contrast to the lower limit.
        and update the display.
        """
        self.value -= self.inc
        if self.value < self.min:
            self.value = self.min
        cfa.api.set_contrast(self.value)
        self.render(self.row, cfa)

    def __init__ (self, line):
        line['vbar_max'] = 255
        line['vbar_min'] = 0
        line['vbar_inc'] = 4
        super(ValueBarContrast, self).__init__(line)
        self.get_value()
        return None

class ValueBarBrightness(ValueBar):
    """
    A valueBar module updated to manage brightness
    """

    def increment(self, cfa):
        """ Increment Brightness to the upper limit.
        and update the display.
        """
        self.value += self.inc
        if self.value > self.max:
            self.value = self.max
        cfa.api.set_backlight(self.value)
        self.render(self.row, cfa)

    def decrement(self, cfa):
        """ deccrement Brightness to the lower limit.
        and update the display.
        """
        self.value -= self.inc
        if self.value < self.min:
            self.value = self.min
        cfa.api.set_backlight(self.value)
        self.render(self.row, cfa)

    def __init__ (self, line):
        line['vbar_max'] = 100
        line['vbar_min'] = 0
        line['vbar_inc'] = 2
        super(ValueBarBrightness, self).__init__(line)
        self.get_value()
        return None

class ServiceLine(Line):
    """
    A Menu class that takes a list of services and dislays the current status of that service.
    """
    def render(self, row, cfa):
        """
        Get Service status and render the line text
        """
        self.row = row
        self.cfa = cfa
        command = "service "+self.service+" status"
        text = os.popen(command).read().rstrip()
        text = self.cfa_bs.pad(text, 20)
        self.cfa.api.set_text(self.row, 0, text)

    def __init__ (self, service):
        super(ServiceLine, self).__init__(service)
        self.service = service
        return None
