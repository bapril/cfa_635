"""
Display a set of static content.
"""
import time
from cfa635.ByteString import ByteString

class Page:
    """
    Pages are static content that will changed based on a pause timer
    or user input. They can also be used for simple animation.
    """
    page = {}

    def render_led(self, cfa):
        """ SET any configured LEDs.
        """
        if 'led1' in self.page:
            cfa.set_led(0, self.page['led1'][0], self.page['led1'][1])

        if 'led2' in self.page:
            cfa.set_led(1, self.page['led2'][0], self.page['led2'][1])

        if 'led3' in self.page:
            cfa.set_led(2, self.page['led3'][0], self.page['led3'][1])

        if 'led4' in self.page:
            cfa.set_led(3, self.page['led4'][0], self.page['led4'][1])

    def render_text(self, cfa):
        """ If we have text, send it.
        """
        if 'line1' in self.page:
            cfa.api.set_text(0, 0, self.cfa_bs.render(self.page['line1']))

        if 'line2' in self.page:
            cfa.api.set_text(1, 0, self.cfa_bs.render(self.page['line2']))

        if 'line3' in self.page:
            cfa.api.set_text(2, 0, self.cfa_bs.render(self.page['line3']))

        if 'line4' in self.page:
            cfa.api.set_text(3, 0, self.cfa_bs.render(self.page['line4']))

    def render(self, cfa):
        """
        Display the page
        """
        print "Render: ", self.page
        if 'cursor_style' in self.page:
            cfa.api.set_cursor_style(self.page['cursor_style'])

        self.render_led(cfa)

        if 'brightness' in self.page:
            cfa.api.set_backlight(self.page['brightness'])

        if 'contrast' in self.page:
            cfa.api.set_contrast(self.page['contrast'])

        self.render_text(cfa)

        if 'pause' in self.page:
            time.sleep(self.page['pause'])

        if 'next' in self.page:
            return self.page['next']
        else:
            return None

    def __init__ (self, page):
        self.page = page
        self.cfa_bs = ByteString()
        return None
