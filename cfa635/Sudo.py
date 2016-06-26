"""
Ask for password/code before passing to the next item.
"""
from cfa635.ByteString import ByteString


class Sudo:
    """
    Require a proper code in order to pass to the next item
    else fall back.
    """

    def run(self, cfa):
        """
        Render/get input loop

        Can return render can return one of:
            True: keep going
            False: return
        """
        key = 0
        key_last = 0
        self.render(cfa)
        while True:
            self.render(cfa)
            if self.code_index == self.code_len:
                return self.success
            (now, _press, _release) = cfa.api.read_keypad()
            key = ord(now)
            if key != key_last:
                if self.code[self.code_index] != key:
                    self.success = False
                self.code_index += 1
                key_last = key

    def render(self, cfa):
        """
        Display the code input.
        """
        if self.setup == False:
            cfa.api.set_text(0, 0, "Authenticate:       ")
            cfa.api.set_text(1, 0, "                    ")
            cfa.api.set_text(2, 0, " Code:              ")
            cfa.api.set_text(3, 0, "                    ")
            i = 0
            while i < (self.code_len):
                cfa.api.set_text(2, 7 + i, self.cfa_bs.render("#d031"))
                i += 1
            self.setup = True

        if self.last_code_index != self.code_index:
            cfa.api.set_text(2, 7 + self.last_code_index, "*")
            self.last_code_index = self.code_index

        if self.code_index > self.code_len:
            if self.success == True:
                cfa.api.set_text(1, 0, " Success!", 19)
            else:
                cfa.api.set_text(1, 0, " Auth Failed", 19)

        #Set Cursor
        cfa.api.set_cursor_position(7 + self.code_index, 2)

        return True

    def __init__ (self, _cfg, menu):
        self.setup = False
        self.cfa_bs = ByteString()
        self.code = menu['code']
        self.code_len = len(self.code)
        self.code_index = 0
        self.last_code_index = 0
        self.success = True
        return None
