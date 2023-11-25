"""
Polyglot v3 node server
Copyright (C) 2023 Steven Bailey
MIT License
"""
import udi_interface
import sys
import time
import urllib3
import asyncio
from bascontrolns import Device, Platform

LOGGER = udi_interface.LOGGER


class bas6uNode(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, ip, ip1, ip2, ip3, ip4, ip5, bc):
        super(bas6uNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)
        self.bc = bc
        LOGGER.info(address)
        # IP Address Sorter
        if address == 'zone_{}'.format(0):
            self.ipaddress = ip
        elif address == 'zone_{}'.format(1):
            self.ipaddress = ip1
        elif address == 'zone_{}'.format(2):
            self.ipaddress = ip2
        elif address == 'zone_{}'.format(3):
            self.ipaddress = ip3
        elif address == 'zone_{}'.format(4):
            self.ipaddress = ip4
        elif address == 'zone_{}'.format(5):
            self.ipaddress = ip5
        else:
            pass

    def start(self):
        if self.ipaddress is not None:
            # Which Device is installed BASpi-Edge-6u6r or BASpi-6u6r
            self.bc = Device(self.ipaddress)
            if self.bc.ePlatform == Platform.BASC_NONE:
                LOGGER.info('Unable to connect')
            elif self.bc.ePlatform == Platform.BASC_PI:
                LOGGER.info('connected to BASpi6U6R')
            elif self.bc.ePlatform == Platform.BASC_ED:
                LOGGER.info('connected to BASpi-Edge-6U6R Module')
                LOGGER.info(str(self.bc.uiQty) +
                            ' Universal inputs in this BASpi')
                LOGGER.info(str(self.bc.boQty) +
                            ' Binary outputs in this BASpi')
                LOGGER.info("BASpiPool IO Points configured")
            else:
                pass
            if self.bc.ePlatform == Platform.BASC_PI or self.bc.ePlatform == Platform.BASC_ED:
                self.setDriver("ST", 1)
            else:
                self.setDriver("ST", 0)

            # Input Output Status
            # Universal Inputs Status
            LOGGER.info("Input 1: " + str(self.bc.universalInput(1)))
            LOGGER.info("Input 2: " + str(self.bc.universalInput(2)))
            LOGGER.info("Input 3: " + str(self.bc.universalInput(3)))
            LOGGER.info("Input 4: " + str(self.bc.universalInput(4)))
            LOGGER.info("Input 5: " + str(self.bc.universalInput(5)))
            LOGGER.info("Input 6: " + str(self.bc.universalInput(6)))

            # Binary/Digital Outputs Status
            LOGGER.info("Output 1: " + str(self.bc.binaryOutput(1)))
            LOGGER.info("Output 2: " + str(self.bc.binaryOutput(2)))
            LOGGER.info("Output 3: " + str(self.bc.binaryOutput(3)))
            LOGGER.info("Output 4: " + str(self.bc.binaryOutput(4)))
            LOGGER.info("Output 5: " + str(self.bc.binaryOutput(5)))
            LOGGER.info("Output 6: " + str(self.bc.binaryOutput(6)))

        ### Universal Inputs ###
        self.setInputDriver('GV0', 1)
        self.setInputDriver('GV1', 2)
        self.setInputDriver('GV2', 3)
        self.setInputDriver('GV3', 4)
        self.setInputDriver('GV4', 5)
        self.setInputDriver('GV5', 6)

    ### Universal Input Conversion ###
    def setInputDriver(self, driver, iIndex):
        input_val = self.bc.universalInput(iIndex)
        count = 0
        if input_val is not None:
            count = float(input_val)
            self.setDriver(driver, count)
        if input_val == "nan":
            count = float(input_val)
            self.setDriver(driver, 0)
        else:
            return

        ### Binary/Digital Outputs ###
        self.setOutputDriver('GV6', 1)
        self.setOutputDriver('GV7', 2)
        self.setOutputDriver('GV8', 3)
        self.setOutputDriver('GV9', 4)
        self.setOutputDriver('GV10', 5)
        self.setOutputDriver('GV11', 6)

    ### Binary Output Conversion ###
    def setOutputDriver(self, driver, input):
        output_val = self.bc.binaryOutput(input)
        count = 0
        if output_val is not None:
            count = (output_val)
            self.setDriver(driver, count)
        else:
            return
        pass

    def setOnOff(self, command=None):
        # Input Output Control
        self.mapping = {
            'DON1': {'output': 'GV6', 'index': (1)},
            'DON2': {'output': 'GV7', 'index': (2)},
            'DON3': {'output': 'GV8', 'index': (3)},
            'DON4': {'output': 'GV9', 'index': (4)},
            'DON5': {'output': 'GV10', 'index': (5)},
            'DON6': {'output': 'GV11', 'index': (6)},
        }
        index = self.mapping[command['cmd']]['index']
        control = self.mapping[command['cmd']]['output']
        output = self.mapping[command['cmd']]['output']
        self.ctrl = int(command.get('value',))
        self.setDriver(control, self.ctrl)
        if self.ctrl == 1:
            self.bc.binaryOutput(index, 1)
            self.setDriver(output, 1)
            LOGGER.info('Output On')
        elif self.ctrl == 0:
            self.bc.binaryOutput(index, 0)
            self.setDriver(output, 0)
            LOGGER.info('Output Off')

    def poll(self, polltype):
        if 'longPoll' in polltype:
            LOGGER.debug('longPoll (node)')
        else:
            self.start()
            LOGGER.debug('shortPoll (node)')

    def query(self, command=None):
        self.start()
        self.reportDrivers()
        LOGGER.info(self.bc)

    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
        {'driver': 'GV0', 'value': 1, 'uom': 56},
        {'driver': 'GV1', 'value': 1, 'uom': 56},
        {'driver': 'GV2', 'value': 1, 'uom': 56},
        {'driver': 'GV3', 'value': 1, 'uom': 56},
        {'driver': 'GV4', 'value': 1, 'uom': 56},
        {'driver': 'GV5', 'value': 1, 'uom': 56},
        {'driver': 'GV6', 'value': 1, 'uom': 80},
        {'driver': 'GV7', 'value': 1, 'uom': 80},
        {'driver': 'GV8', 'value': 1, 'uom': 80},
        {'driver': 'GV9', 'value': 1, 'uom': 80},
        {'driver': 'GV10', 'value': 1, 'uom': 80},
        {'driver': 'GV11', 'value': 1, 'uom': 80},

    ]

    id = 'zone'

    commands = {
        'DON1': setOnOff,
        'DON2': setOnOff,
        'DON3': setOnOff,
        'DON4': setOnOff,
        'DON5': setOnOff,
        'DON6': setOnOff,
        'PING': query
    }
