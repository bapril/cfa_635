"""
Master CFA 635 Module
"""
from cfa635.ByteString import ByteString
from cfa635.Page import Page
from cfa635.Line import Line
from cfa635.Line import ServiceLine
from cfa635.Sudo import Sudo

import os

class Item:
    """
    Generic container class for items/actions
    Anything that can be done/displayed on a
    CFA635 starts here
    """
    page = {}

    def render(self, cfa):
        """
        Route the item to the appropriate processing code.
        """
        if 'type' in self.item:
            if self.item['type'] == 'page':
                page = Page(self.item)
                return page.render(cfa)
            elif self.item['type'] == 'page_wait_for_input':
                page = Page(self.item)
                out = page.render(cfa)
                cfa.flush_key_input()
                my_input = cfa.wait_for_input(1000)
                if my_input == False:
                    cfa.go_to_sleep()
                    cfa.sleep_wait_for_input()
                    cfa.wake_up()
                return out
            elif self.item['type'] == 'menu':
                menu = Menu(self.cfg, self.item)
                return menu.run(cfa)
            elif self.item['type'] == 'service_menu':
                service_menu = ServiceMenu(self.cfg, self.item)
                return service_menu.run(cfa)
            elif self.item['type'] == 'sudo':
                sudo_menu = Sudo(self.cfg, self.item)
                if sudo_menu.run(cfa) == True:
                    item = Item(self.cfg,self.item['next_action'])
                    item.render(cfa)
            else:
                raise Exception("Item Type is Unknown. ",self.item['type'])
        else:
            raise Exception("Item has no Type")

    def __init__ (self, cfg, item):
        #TODO don't crash if item doesn't exist
        self.item = cfg[item]
        self.cfg = cfg
        return None

class Menu:
    """
    Menu generator module for the CFA635 LCD system
    """

    menu = {}
    state = {}
    line_list = []

    def load_lines(self):
        """
        Pre-load the lines for this menu into memory.
        """
        self.line_list = [] #It's important to re-zero before loading
        if 'first_line' in self.menu:
            line = self.menu['first_line']
        else:
            raise Exception("Menu must have a fist_line")
        while(line != None):
            i = Line(self.menu['lines'][line])
            self.line_list.append(i.route())
            if 'next_line' in self.menu['lines'][line]:
                line = self.menu['lines'][line]['next_line']
            else:
                line = None

    def run(self, cfa):
        """
        Render/get input loop

        Can return render can return one of:
            True: keep going
            False: return
        """

        key = 0
        self.render(cfa, key)
        while True:
            keep_going = self.render(cfa, key)
            if keep_going != True:
                return
            need_input = True
            while need_input:
                (my_input, key) = cfa.get_input(1000)
                if my_input == False:
                    cfa.go_to_sleep()
                    cfa.sleep_wait_for_input()
                    cfa.wake_up()
                else:
                    need_input = False


    def calculate_title(self, title, size):
        """
        Add padding to center title, and truncate when needed
        to fit on one line.
        """
        length = self.cfa_bs.length(title)
        if length == size:
            return title
        elif length > size:
            return self.cfa_bs.render(title)[:size]
        else:
            gap = size - length
            if gap % 2 != 0: # Odd
                title += " "
                gap -= 1
            if gap > 0:
                gap = gap / 2
                pad = ""
                while gap:
                    pad += " "
                    gap -= 1
                title = pad+title+pad
        return title

    def get_row(self):
        """
        Determine which of the 3 lines we should be interacting
        with give our cursor and view index
        """
        row = (self.state['cursor_index'] - self.state['view_index']) + 1
        return row

    def get_scroll_indicator(self):
        """
        By comapring the size of the line list and our current
        view index we can tell if we have room to scroll up or
        down
        """

        #Set scroll-indicator
        if len(self.line_list) < 4:
            return " "
        else:
            if self.state['view_index'] == 0:
                return "#d027" #Down Arrow
            else:
                if self.state['view_index'] == (len(self.line_list) - 3 ):
                    return "#d026" #Up Arrow
                else:
                    return "#d148" #diamond

    def move_up(self, cfa):
        """
        Keypress was up, update the menu and redraw if needed
        """
        #At Top
        if self.state['cursor_index'] == 0:
            if self.menu['endless'] :
                self.state['cursor_index'] = len(self.line_list) - 1
                self.state['view_index'] = len(self.line_list) - 3
                return True
        else:
            #remove old arrow
            row = self.get_row()
            cfa.api.set_text(row, 19, self.cfa_bs.render(" "))

            #decrement cursor index
            self.state['cursor_index'] -= 1

            #Evaluate view_index
            if self.state['cursor_index'] < (self.state['view_index']):
                self.state['view_index'] -= 1
                return True
        return False

    def move_down(self, cfa):
        """
        Keypress was down, update the menu and redraw as needed
        """

        #At Bottom
        if self.state['cursor_index'] == (len(self.line_list) - 1):
            if self.menu['endless'] :
                self.state['cursor_index'] = 0
                self.state['view_index'] = 0
                return True
        else:

            #remove old arrow
            row = self.get_row()
            cfa.api.set_text(row, 19, self.cfa_bs.render(" "))

            #Incerement cursor index
            self.state['cursor_index'] += 1

            #Evaluate view_index
            if self.state['cursor_index'] == (self.state['view_index'] + 3):
                self.state['view_index'] += 1
                return True
        return False

    def render_line(self, line):
        """
        Given an line config,
        render/find/generate/calculate the text to appear
        """
	if 'line_type' in line:
            print "Line Type: "+line['line_type']
	    return "Type: "+line['line_type']
        elif 'line_text' in line:
            return self.cfa_bs.pad(line['line_text'], 20)
        elif 'line_cmd' in line:
            text = os.popen(line['line_cmd']).read().rstrip()
            return self.cfa_bs.pad(text, 20)
        else:
            print "HELP"
	    return "help"

    def process_key(self, cfa, key):
        """ Handle key press
        """
        #TODO Map row to Line, pass key, act accordingly
        (action_taken,next_action) = self.line_list[self.state['cursor_index']].process_key(key, cfa)
        if action_taken == True:
            #Item took the keypress,
            if next_action != None:
                #We have an action that we need to trigger
                row = self.get_row()
                cfa.api.set_text(row, 19, self.cfa_bs.render(" "))
                cfa.api.set_cursor_style(cfa.CURSOR_NO)

                item = Item(self.cfg, next_action)
                item.render(cfa)
                self.state['title_sent'] = False
            return(False,False)
        else:
            #The item does not want this keypress, we handle it.
            if key:
                if key == cfa.KEY_UP:
                    return (False, self.move_up(cfa))
                elif key == cfa.KEY_DOWN:
                    return (False, self.move_down(cfa))
                elif key == cfa.KEY_LEFT or key == cfa.KEY_STOP:
                    self.state['view_index'] = 0
                    self.state['cursor_index'] = 0
                    return (True, False)
                elif key == cfa.KEY_RIGHT or key == cfa.KEY_OK:
                    line = self.line_list[self.state['cursor_index']]
                    if 'action' in line.line:
                        action = line.line['action']
                        row = self.get_row()
                        cfa.api.set_text(row, 19, self.cfa_bs.render(" "))
                        cfa.api.set_cursor_style(cfa.CURSOR_NO)

                        item = Item(self.cfg, action)
                        item.render(cfa)
                        self.state['title_sent'] = False
                    return (False, False)
            else:
                return (False, False)

    def render(self, cfa, key):
        """
        Take the provided key input, process it in relation
        the menu in state, re-render as appropriate.
        """
        (term, redraw) = self.process_key(cfa, key)
        if term == True:
          return False

        if 'title' in self.menu:
            if self.state['title_sent'] == False:
                #If we haven't displayed the title, we have to draw everyting
                redraw = True
                cfa.api.set_text(0, 0, \
                    self.calculate_title(self.menu['title'], 19))
                self.state['title_sent'] = True
        else:
            raise Exception("Menu must have a title")

        if redraw:
            cfa.api.set_text(0, 19, \
                self.cfa_bs.render(self.get_scroll_indicator()))

            #present lines
            self.line_list[self.state['view_index']].render(1,cfa)
            if len(self.line_list) > 1:
                self.line_list[self.state['view_index'] + 1].render(2,cfa)
                if len(self.line_list) > 2:
                    self.line_list[self.state['view_index'] + 2].render(3,cfa)
                else:
                    cfa.api.set_text(3, 0, self.cfa_bs.pad(" ", 20))
            else:
                cfa.api.set_text(2, 0, self.cfa_bs.pad(" ", 20))
                cfa.api.set_text(3, 0, self.cfa_bs.pad(" ", 20))

        #Set Cursor
        row = self.get_row()
        cfa.api.set_text(row, 19, self.cfa_bs.render("#d225"))
        cfa.api.set_cursor_position(19, row)

        return True

    def __init__ (self, cfg, menu):
        self.menu = menu
        self.state['view_index'] = 0
        self.state['cursor_index'] = 0
        self.state['title_sent'] = False
        self.load_lines()
        self.cfg = cfg
        self.cfa_bs = ByteString()
        return None

"""
Functions for support of linux service menus.
"""
from cfa635.ByteString import ByteString
from cfa635.CFA635 import Menu
import os

class ServiceMenu(Menu):
    """
    Generate a menu based on running services
    """

    def load_lines(self):
        """
        Pre-load the lines for this menu into memory.
        """
        self.line_list = [] #It's important to re-zero before loading
        for service in self.menu['services']:
          i = ServiceLine(service)
          self.line_list.append(i.route())
