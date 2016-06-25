#!/usr/bin/python
"""
Test library to execute CFA-635 controller code
"""

import sys, getopt, yaml
from cfa635.Device import Device
from cfa635.Controller import Controller

def usage():
    """
    Display usage
    """
    print 'main.py [-v] -c <configfile>'
    print '\n'
    print '-v --verbose   - Enable extra STDOUT output'
    print '-c --config    - Config file (required)'
    print '-h --help      - this help'

def main(argv):
    """
    Run the test.
    """

    configfile = ''
    verbose = 0
    try:
        opts, _args = getopt.getopt(argv, "hvc:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt == '-v':
            verbose += 1
            print "Verbose set to: ", verbose
        elif opt in ("-c", "--config"):
            configfile = arg
    if configfile == '':
        print "Error: Config file not specified\n"
        usage()
        sys.exit()

    with open(configfile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    if verbose > 0:
        cfg['verbosity'] = verbose
        print "Starting LCD Interface:"

    dev = Device(cfg)
    cfa = Controller(dev)

    #0x00
    cfa.api.ping(None)
    cfa.api.ping("Foobar")

    #0x01
    print "Firmware Version: ", cfa.api.get_firmware_version()

    #0x02 - #0x03
    print "Flash Area: ", cfa.api.read_user_flash()
    cfa.api.write_user_flash("TEST 12345678901")
    print "Flash Area: ", cfa.api.read_user_flash()

    #0x04
    cfa.api.set_boot_state()

    #0x05
    #cfa.api.reboot()

    #0x06
    cfa.api.clear_screen()

    data = chr(63)+chr(31)+ chr(15) + chr(7) + chr(3) + chr(1) + chr(0) + chr(0)
    cfa.api.set_cg_data(0, data)

    (index, data) = cfa.api.get_cg_data(64)
    print "Index: ", ord(index)
    print "Data: ", ord(data[0])
    print "Data: ", ord(data[1])
    print "Data: ", ord(data[2])
    print "Data: ", ord(data[3])
    print "Data: ", ord(data[4])
    print "Data: ", ord(data[5])
    print "Data: ", ord(data[6])
    print "Data: ", ord(data[7])

    cfa.api.set_cursor_position(10, 2)
    cfa.api.set_cursor_style(cfa.CURSOR_INV_BLINK_UNDER)

    cfa.api.set_backlight(50)
    cfa.api.set_contrast(128)

    cfa.api.set_text(0, 0, "This Is A Test")
    cfa.set_led(0, 0, 0)
    cfa.set_led(1, 100, 0)
    cfa.set_led(2, 50, 50)
    cfa.set_led(3, 0, 100)

    dev.close()

if __name__ == "__main__":
    main(sys.argv[1:])
