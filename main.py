#!/usr/bin/python
"""
Script to run a menu on the CFA635
"""

import sys, getopt, yaml
from cfa635.Device import Device
from cfa635.Controller import Controller
from cfa635.CFA635 import Item
from cfa635.LEDSet import LEDSet


def usage():
    """
    Display usage
    """
    print 'main.py [-v] -c <configfile>'
    print '\n'
    print '-v --verbose   - Enable extra STDOUT output'
    print '-c --config    - Config file (required)'
    print '-r --root      - root item to start, default config\'s root:item'
    print '-h --help      - this help'
    print '-s --setup     - Setup LCD with defaults'

def main(argv):
    """
    Run the menu
    """
    config_file = ''
    start_root = None
    verbose = 0
    setup = False
    try:
        opts, _args = getopt.getopt(argv, "hvsc:r:", ["config=", "root="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-s", "--setup"):
            setup = True
        elif opt in ('-v', "--verbose"):
            verbose += 1
            print "Verbose set to: ", verbose
        elif opt in ("-c", "--config="):
            config_file = arg
        elif opt in ("-r", "--root"):
            start_root = arg
    if config_file == '':
        print "Error: Config file not specified\n"
        usage()
        sys.exit()

    with open(config_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    if verbose > 0:
        cfg['verbosity'] = verbose

    if verbose > 0:
        for section in cfg:
            print "config section: ", section
            if verbose > 1:
                for item in cfg[section]:
                    print item, "Value: ", cfg[section][item]

    if verbose > 0:
        print "Starting LCD Interface:"
    dev = Device(cfg)
    cfa = Controller(dev)
    led = LEDSet(cfa,cfg)
    cfa.register_led_callback(led)

    with open(cfg['root']['defaults'], 'r') as ymlfile:
        def_cfg = yaml.load(ymlfile)
    if 'brightness' in def_cfg:
        print "Set Brightness to: ",def_cfg['brightness']
        cfa.api.set_backlight(int(def_cfg['brightness']))
    if 'contrast' in def_cfg:
        print "Set Contrast to: ",def_cfg['contrast']
        cfa.api.set_contrast(int(def_cfg['contrast']))

    #0x00
    cfa.api.ping(None)
    #0x01
    print "Firmware Version: ", cfa.api.get_firmware_version()

    # Setup screen
    if setup == True:
        print "Setting Power-on defaults"
        cfa.api.clear_screen()
        cfa.set_led(0, 0, 0)
        cfa.set_led(1, 0, 0)
        cfa.set_led(2, 0, 0)
        cfa.set_led(3, 0, 0)
        cfa.api.set_key_reporting(0, 0)
        cfa.api.set_boot_state()
        dev.close()
        sys.exit()

    while True:
        if start_root == None:
            start_root = cfg['root']['item']
        else:
            if start_root not in cfg['items']:
	      raise Exception("Start_root "+start_root+" does not exist")
        item = Item(cfg['items'], start_root)
        while item != None:
            next_item = item.render(cfa)
            if next_item != None:
                if next_item in cfg['items']:
                    item = Item(cfg['items'], next_item)
                else:
                    item = Item(cfg['items'], cfg['root']['item'])
            else:
                item = None

    dev.close()

if __name__ == "__main__":
    main(sys.argv[1:])
