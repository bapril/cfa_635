"""
Support Low-level communications with the CFA-635
"""

import serial, sys, time
from cfa635.Packet import Packet

class Device:
    """
    This is where we will handle low-level communication with the device. Input and output.
    """

    serial = None
    inbound_callback = None

    def __init__(self, config):
        self.config = config

        self.serial = serial.Serial(config['device']['port'])
        serial_settings = self.serial.getSettingsDict()
        if config['verbosity'] > 3:
            print "Default Serial Settings: ", serial_settings
        for key in serial_settings:
            if key in config['device']:
                serial_settings[key] = config['device'][key]
        if config['verbosity'] > 2:
            print "Serial Settings: ", serial_settings
        self.serial.applySettingsDict(serial_settings)

        try:
            self.serial.open()
        except serial.SerialException:
            print("Unexpected error:", sys.exc_info()[0])
        except Exception:
            raise

        if self.serial.readable() != True:
            print "Serial port not readable"
            raise

    def receieve_packet (self):
        """
        Receieve packe from CFA635 serial interface.
        Parse it into the appropriate structure
        """
        output = Packet()
        while output.retry_count < 15 and output.cmd == None:
            output.cmd = self.serial.read(1)
            time.sleep(0.02)
            output.increment_retry()

        if output.cmd == None or output.cmd == "" :
            output.set_error("Unable to receive message type part")
            return output

        output.len = ord(self.serial.read(1))
        if output.len == None  or output.len == ""  :
            output.set_error("Unable to receive message length part")
            return output

        output.data = self.serial.read( output.len )
        if output.len != len(output.data):
            output.set_error("Length doens't match data")
            return output

        output.crc = self.serial.read(2)

        if output.crc == None or len(output.crc) < 2    :
            output.set_error("Didn't get entire CRC")

        return output


    def send_packet (self, packet):
        """
        Marshall and send a packet to the CFA635
        """
        if packet.len != 0:
            if len(packet.data) != packet.len:
                raise Exception("Error LEN and payload don't match")

        if self.serial.writable() != True:
            raise Exception("Serial port not writable")

        self.serial.write(packet.tx_packet())
        self.serial.flush()
        time.sleep(0.01)

        reply = self.receieve_packet()
        if reply.is_error:
            raise Exception(reply.error)
        if ord(reply.cmd) != ord(packet.cmd) | 0x40:
            raise Exception("Reply is not for me ", ord(reply.cmd))

        return  reply

    def close (self):
        """
        Close the serial connection
        """
        self.serial.flush()
        self.serial.close()
