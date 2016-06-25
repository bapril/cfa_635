#pylint: disable=R0904
""" Module containing functions for every activity availiable in the CFA635 API
"""
from cfa635.Packet import Packet

class API:
    """ Class driving the LCD with easy to call functions
    """

    dev = None
    backlight_set = 0
    backlight_current = 0

    def __init__ (self, dev):
        self.dev = dev
        return None

    def ping(self, payload):
        """ #0 (0x00): Ping Command
        """
        packet = Packet()
        packet.cmd = "\x00"
        if payload == None:
            packet.len = 0
        else:
            packet.len = len(payload)
            packet.data = payload
        reply = self.dev.send_packet(packet)
        if reply.len != packet.len:
            raise Exception("Packet lengths don't match")
        if reply.len > 0:
            if reply.data != packet.data:
                raise Exception("Packet payload dosn't match")

    def get_firmware_version(self):
        """ #1 (0x01): Get Hardware & Firmware Version
        """
        packet = Packet()
        packet.cmd = "\x01"
        packet.len = 0
        reply = self.dev.send_packet(packet)
        return reply.data

    def write_user_flash(self, data):
        """ #2 (0x02): Write User Flash Area
        """
        packet = Packet()
        packet.cmd = "\x02"
        packet.data = data
        packet.len = len(data)
        if packet.len != 16:
            raise Exception("Flash Write must be exacty 16 bytes")
        self.dev.send_packet(packet)

    def read_user_flash(self):
        """ #3 (0x03): Read User Flash Area
        """
        packet = Packet()
        packet.cmd = "\x03"
        reply = self.dev.send_packet(packet)
        return reply.data

    def set_boot_state(self):
        """ #4 (0x04): Store Current State As Boot State
        """
        packet = Packet()
        packet.cmd = "\x04"
        self.dev.send_packet(packet)

    def reboot(self):
        """ #5 (0x05): Reboot XES635BK-xxx-KU
        """
        packet = Packet()
        packet.cmd = "\x05"
        packet.len = 3
        packet.data = (chr(8) + chr(18) + chr(99))
        self.dev.send_packet(packet)

    def clear_screen(self):
        """ #6 (0x06): Clear LCD Screen
        """
        packet = Packet()
        packet.cmd = "\x06"
        packet.len = 0
        self.dev.send_packet(packet)

#7 0x07 Deprecated
#8 0x08 Deprecated
    def set_cg_data(self, index, data):
        """ #9 (0x09): Set LCD Special Character Data
        """
        #TODO validate type of data
        if len(data) != 8:
            raise Exception("Data should be 8 bytes")

        packet = Packet()
        packet.cmd = "\x09"
        packet.len = 9
        packet.data = (chr(index) + data)
        self.dev.send_packet(packet)

    def get_cg_data(self, index):
        """ #10 (0x0A): Read 8 Bytes of LCD Memory
        """
        packet = Packet()
        packet.cmd = "\x0A"
        packet.len = 1
        packet.data = chr(index)
        reply = self.dev.send_packet(packet)
        return (reply.data[0], reply.data[1:9])

    def set_cursor_position(self, col, row):
        """ #11 (0x0B): Set LCD Cursor Position
        """
        packet = Packet()
        packet.cmd = "\x0B"
        packet.len = 2
        packet.data = (chr(col) + chr(row))
        self.dev.send_packet(packet)

    def set_cursor_style(self, style):
        """ #12 (0x0C): Set LCD Cursor Style
        """
        packet = Packet()
        packet.cmd = "\x0C"
        packet.len = 1
        packet.data = chr(style)
        self.dev.send_packet(packet)

    def set_contrast(self, contrast):
        """ #13 (0x0D): Set LCD Contrast
        """
        packet = Packet()
        packet.cmd = "\x0D"
        packet.len = 1
        packet.data = chr(contrast)
        self.dev.send_packet(packet)

    def set_backlight(self, backlight):
        """ #14 (0x0E): Set LCD & Keypad Backlight
        """
        packet = Packet()
        packet.cmd = "\x0E"
        packet.len = 1
        packet.data = chr(backlight)
        self.backlight_current = backlight
        self.dev.send_packet(packet)

#15 (0x0F): Deprecated
#16 (0x10): Not Supported (Set Up Fan Reporting)
#17 (0x11): Not Supported (Set Fan Power)
#18 (0x12): Not Supported (Read WR-DOW-Y17 Temperature Sensors)
#19 (0x13): Not Supported (Set Up WR-DOW-Y17 Temperature Reporting)
#20 (0x14): Not Supported (Arbitrary DOW Transaction)
#21 (0x15): Deprecated
#22 (0x16): Send Command Directly to the LCD Controller
    def set_key_reporting (self, press, release):
        """ #23 (0x17): Configure Key Reporting
        """
        packet = Packet()
        packet.cmd = "\x17"
        packet.len = 2
        packet.data = chr(press) + chr(release)
        self.dev.send_packet(packet)

    def read_keypad(self):
        """ #24 (0x18): Read Keypad, Polled Mode
        """
        packet = Packet()
        packet.cmd = "\x18"
        packet.len = 0
        reply = self.dev.send_packet(packet)
        return (reply.data[0], reply.data[1], reply.data[2])

#25 (0x19): Not Supported (Set Fan Power Fail-Safe)
#26 (0x1A): Not Supported (Set Fan Tachometer Glitch Filter)
#27 (0x1B): Not Supported (Query Fan Power & Fail-Safe Mask)
#28 (0x1C): Not Supported (Set ATX Power Switch Functionality)
#29 (0x1D): Not Supported (Enable/Disable and Reset the Watchdog)
#30 (0x1E): Read Reporting & Status
    def set_text( self, row, col, text):
        """
        #31 (0x1F): Send Data to LCD
        """
        if len(text) > ( 21 - col):
            raise Exception("Text runs over end.")
        packet = Packet()
        packet.cmd = "\x1F"
        packet.data = chr(col) + chr(row)
        packet.data += text
        packet.len = len(packet.data)
        self.dev.send_packet(packet)

#32 (0x20): Reserved for CFA631 Key Legends
#33 (0x21): Set Baud Rate
    def set_gpio(self, pin, value):
        """
        #34 (0x22): Set GPO Pin
        """
        packet = Packet()
        packet.cmd = "\x22"
        packet.len = 2
        packet.data = chr(pin) + chr(value)
        self.dev.send_packet(packet)

#35 (0x23): Not Supported (Read GPIO and GPO Pin Levels and Configuration State)
