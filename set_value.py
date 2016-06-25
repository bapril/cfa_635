#!/usr/bin/python
"""
Set values to the defaults files.
"""

import sys, getopt, yaml

def usage():
    """
    Display usage
    """
    print 'get_value.py key value'
    print 'key            - Which value to read'
    print 'value          - Value to set int he defaults'

def main(argv):
    """
    Run the menu
    """
    key = None
    value = None
    config_file = './config/defaults.conf'
    if len(argv) == 2:
      key = argv[0]
      value = argv[1]
    else:
      usage()
      sys.exit()

    with open(config_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    cfg[key] = value

    with open(config_file, 'w') as yamlfile:
        yamlfile.write( yaml.dump(cfg))

if __name__ == "__main__":
    main(sys.argv[1:])
