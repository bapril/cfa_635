# CFA-635 Event driven menu system

Early commit of a CFA 635 library for python. The goal is to create a fully event-driven menu system that's simple to use and powerful.

## Configuration:

* The Main config file contains the following sections:
  1. verbosity: single value 0 for normal up to 5 for debug
  1. device: contains port and baudrate settings:

  ```yaml
device:
  port: /dev/cu.usbserial-CF003400
  baudrate: 115200
```

  1. root: Contains the defaults file, sudo code and starting item:

  ```yaml
root:
  defaults: config/defaults.conf
  item: s1
```

  The Defaults config file contains values that can be changed by users via the cfa635, for example brightness, contrast, and screen timeout.  see the defaults.conf.dist for an example.

  1. items: Menu items, pages and lines.
    * Menu: A menu is an ordered set of menu Lines.

    ```yaml
items:
  main_menu:
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
        action: admin_menu
```

    * Lines: Lines are menu items. Each type of line supports a different behavior.
      * Line: The basic line class displays a `line_text` and excutes the item `action` when selected.

      ```yaml
   status_menu:
     line_text: "Status"
     next_line: services_menu
     action: status_menu
```

      * CmdLine: Command Lines display the output of a shell command as their text. Remember you only have 20 chars to work with.

      ```yaml
   disk_free_slash:
     line_type: cmd_line
     line_cmd: "df / -h | tail -1 | awk {'print \"Disk / Avail: \"$4'}"
     next_line: uptime
```

      * ValueBar: When selected the user can move right/up or left/down to adjust the value of the bar. Enter will save the value, exit will abort. The value is set at display time with vbar_read, and saved with vbar_write. `%v` is replace with the value.

      ```yaml
     lines:
       display_timeout_title:
         line_text: "Screen Timeout:"
         next_line: display_timeout_value
       display_timeout_value:
         line_type: value_bar
         vbar_min: 0
         vbar_max: 255
         vbar_inc: 25
         vbar_read: "./get_value.py timeout"
         vbar_write: "./set_value.py timeout %v"
```

      * ValueBarBrightness: Much like ValueBar, but this version updates the brightness of the screen as the value changes.

      ```yaml
     lines:
       display_timeout_title:
         line_text: "Screen Timeout:"
         next_line: display_timeout_value
       display_timeout_value:
         line_type: value_bar
         vbar_read: "./get_value.py timeout"
         vbar_write: "./set_value.py timeout %v"
```

      * ValueBarContrast: Much like ValueBar however this version updates the screen contrast as the value changes.

      ```yaml
     lines:
       display_contrast_title:
         line_text: "Contrast:"
         next_line: display_contrast_value
       display_contrast_value:
         line_type: value_bar_contrast
         vbar_read: "./get_value.py contrast"
         vbar_write: "./set_value.py contrast %v"
         next_line: display_timeout_title
```
      * SelectLine: Given a dict of options, select one of them. Current state is returned from the command 'select_current_cmd' the value is set with 'select_cmd'

      ```yaml
      ip_mode_select:
        line_text: "IP Mode:"
        line_type: select_line
        options: [prod, open, eng]
        select_cmd: "echo \"%v\" > /tmp/mode"
        select_current_cmd: "cat /tmp/mode"
```
      * Pages: A set of static content that is displayed on the LCD screen. Pages can also drive the LEDs as well brightness and contrast. This page will set 4 lines of text, make all 4 LEDs green and wait for input before executing the item main_menu

      ```yaml
  about_page:
    type: page_wait_for_input
    line1: "#d016#d016#d016 ACME  CENTER #d017#d017#d017"
    line2: "Version 0.1.0       "
    line3: "2016-JUN-24         "
    line4: 'bapril@gmail.com    '
    led1: [100,0]
    led2: [100,0]
    led3: [100,0]
    led4: [100,0]
    next: main_menu
```

## References:
 1. http://www.crystalfontz.com/products/document/1/CFA_635_1_0.pdf
 1. https://www.crystalfontz.com/products/document/3158/XES635BK-xxx-KU_Data_Sheet_2012-12-07.pdf
 1. https://github.com/tbdale/crystalfontz-lcd-ui
 1. https://mail.python.org/pipermail/python-list/2005-September/332594.html

## Dependancies:
 1. python
 1. python-serial
 1. python-yaml
