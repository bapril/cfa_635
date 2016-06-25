"""
Library for handling special chars in strings for display on a CFA-635
@ for example is not where one would expect in the CGmap, so we correct it
and others. We also enable #d000 notation to call specific chars from the
CFA's CGROM
"""

class ByteString:
    """
    Library for handling special chars in strings for display on a CFA-635
    @ for example is not where one would expect in the CGmap, so we correct it
    and others. We also enable #d000 notation to call specific chars from the
    CFA's CGROM
    """

    #"`~!@#$%^&*()_+-={}[]"
    replacement_map = { '~':206, '@': 160, '$': 162, '^': 211, '_': 196,
    '{': 253, '}': 255, '[': 250, ']': 252}


    def render(self, my_input):
        """
        Given an input string, replace any non-printable chars with
        the appropriate CGROM code
        """
        output = ""
        index = 0
        while(index < len(my_input)):
            if my_input[index] in self.replacement_map:
                output += chr(self.replacement_map[my_input[index]])
            elif my_input[index] == '#':
                if my_input[index+1] == '#':
                    output += '#'
                    index += 1
                elif my_input[index+1] == 'd':
                    output += chr((int(my_input[index+2]) * 100)
                        + (int(my_input[index+3]) * 10)
                        + int(my_input[index+4]))
                    index += 4
            else:
                output += my_input[index]
            index += 1
        return output

    def length(self, my_input):
        """
        Return Lenght of the rendered string.
        """
        return len(self.render(my_input))

    def pad(self, source, size):
        """
        Pad a byte-string to the specified size by appending spaces
        this serves to mask the text that came before it.
        """
        my_input = self.render(source)
        output = ""
        index = 0
        while index < size:
            if index < len(my_input):
                output += my_input[index]
            else:
                output += " "
            index += 1
        return output

    def __init__ (self):
        return None
