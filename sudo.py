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
    Generate a SUDO string.
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

    now_last = 0;
    count = 0
    code_length = 12
    code = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    while True:
     print "Create CODE: "
     while count < code_length:
       (now,_press,_release) = cfa.api.read_keypad()
       now = ord(now)
       if now != now_last:
         print "NOW Change Before: ",now_last," Now: ",now
         code[count] = now
         now_last = now
         count += 1
     print "Code = : ",yaml.dump(code)
     tries = 4
     print "Try the code:"
     while tries > 0:
       count = 0
       success = True
       now_last = 0;
       while count < code_length:
         (now,_press,_release) = cfa.api.read_keypad()
         now = ord(now)
         if now != now_last:
           if code[count] != now:
             success = False
           now_last = now
           count += 1
       tries -= 1
       if success:
         print "SUCCESS!"
       else:
         print "Fail!"
     code = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
     count = 0
     now_last = 0;


    dev.close()

if __name__ == "__main__":
    main(sys.argv[1:])
