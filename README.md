# CFA-635 Event driven meny system

Early commit of a CFA 635 library for python. The goal is to create a fully event-driven menu system that's simple to use and powerful.

## Configuration:

  * The Main config file contains the following sections:
    1. verbosity: single value 0 for normal up to 5 for debug
    1. device: contains port and baudrate settings:
    ```port: /dev/cu.usbserial-CF003400
    baudrate: 115200```
    1. root: Contains the defaults file, sudo code and starting item:
    ```defaults: config/defaults.conf
    sudo: [1, 0, 16, 0, 32, 0, 8, 0, 2, 0, 4, 0] # Up, Right, Down, Left, Enter, Stop
    item: s1```
    1. items: Menu items, pages and lines.
  * The Defaults config file contains values that can be changed by users via the cfa635, for example brightness, contrast, and screen timeout.  see the defaults.conf.dist for an example.
  * Menus
``` main_menu:
    type: menu #Tells the parser that we want a menu
    title: "Main Menu" # MUST have a title
    first_line: about_page #Which of the lines below will be the start-point.
    endless: False # If I keep scrolling down will I be taken to the top
    lines: #Set of lines for this menu.
      about_page:
        line_text: "About" #Text to display.
        next_line: setup_menu  # Next line in the lined-list.
        action: about_page #Name of the line to run if selected.
      admin_menu: #The last item will not have a next_line key.
        line_text: "Admin Menu #d171"
        action: admin_menu ```


## References:
 1. http://www.crystalfontz.com/products/document/1/CFA_635_1_0.pdf
 1. https://www.crystalfontz.com/products/document/3158/XES635BK-xxx-KU_Data_Sheet_2012-12-07.pdf
 1. https://github.com/tbdale/crystalfontz-lcd-ui
 1. https://mail.python.org/pipermail/python-list/2005-September/332594.html

## Dependancies:
 1. python
 1. python-serial
 1. python-yaml
