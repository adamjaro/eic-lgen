#!/usr/bin/python

# /usr/bin/python
# /afs/rhic.bnl.gov/eic/bin/python

import sys

from event import event

#_____________________________________________________________________________
if __name__ == "__main__":

    #name of config file from command line argument
    args = sys.argv
    if len(args) < 2:
        print "No configuration specified."
        quit()
    args.pop(0)
    config = args.pop(0)

    #init and run
    event(config)























