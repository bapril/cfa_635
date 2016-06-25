"""
A library for generating and decoding CFA635 packets.
"""
import cfa635.crc16

class Packet:
    """
    A library for generating and decoding CFA635 packets.
    """
    cmd = None
    len = 0
    data = None
    crc = None
    is_error = False
    error = None
    retry_count = 0


    def set_error(self, string):
        """
        There is something wrong with this packet.
        Set an error.
        """
        self.is_error = True
        self.error = string

    def increment_retry(self):
        """
        Keep track of how many times we needed to send
        this packet to be successful
        """
        self.retry_count += 1

    def validate_crc(self):
        """
        Confirm that the CRC matches what would be expected
        given the payload.
        """
        incoming_crc = ord(self.crc[0]) + (ord(self.crc[1]) << 8)
        crc = cfa635.crc16.CRC16()
        crc.update(self.cmd + self.len + self.data)
        if crc.get_value() != incoming_crc:
            self.is_error = True
            self.error = "Invlid CRC"
            return False
        return True

    def generate_payload(self):
        """
        If length is set include payload
        Otherwise the packet is uniary
        """
        if self.len == 0:
            return self.cmd + chr( self.len )
        else:
            return self.cmd + chr( self.len ) + self.data

    def tx_packet(self):
        """
        Calculate and add CRC
        """
        payload = self.generate_payload()
        if self.crc == None:
            crc = cfa635.crc16.CRC16()
            crc.update(payload)
            csum = crc.get_value()
            self.crc = chr(csum & 0x00FF) + chr(csum >> 8)
        return payload + self.crc

    def __init__ (self):
        return None
