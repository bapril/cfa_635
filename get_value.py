#!/usr/bin/python
"""
Gets values form the defaults files.
"""

import sys, getopt, yaml

def usage():
    """
    Display usage
    """
    print 'get_value.py [hv] key'
    print '\n'
    print 'key            - Which value to read'

def main(argv):
    """
    Run the menu
    """
    config_file = './config/defaults.conf'
    if len(argv) == 1:
      key = argv[0]
    else:
      usage()
      sys.exit()

    with open(config_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    print cfg[key]

if __name__ == "__main__":
    main(sys.argv[1:])
