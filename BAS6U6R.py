#!/usr/bin/env python3
"""
Polyglot v3 node server
Copyright (C) 2023 Steven Bailey
MIT License
"""
import udi_interface
import sys

from nodes import bas6u_ctl

LOGGER = udi_interface.LOGGER

if __name__ == "__main__":
    try:
        polyglot = udi_interface.Interface([])
        polyglot.start()

        # Create the controller node
        bas6u_ctl.Controller(polyglot, 'controller',
                             'controller', 'Controller')

        # Just sit and wait for events
        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
