# -*- coding: utf-8 -*-
'''
functions for communication with XMC

This script requires the package "pyserial" NOT the "serial" package,
despite being imported through serial.
Installation: e.g. 'pip install pyserial' in conda prompt

In many cases (e.g. Spyder) the serial port is not closed after program execution.
In such a case one can close the port using the "ser.close()" command.
'''

import numpy as np
import serial
import serial.tools.list_ports
import sys
import base64
from bitstring import Bits
import time


def read_hex(hexstring):
    #hexstring=''.join(reversed(hexstring))
    if len(hexstring) == 999:
       print('error')
    else:
        bx1, bx2 = hexstring[2:4],hexstring[4:6]
        bx =bx2+bx1
        by1,by2 = hexstring[6:8],hexstring[8:10]
        by= by2+by1
        bz1,bz2 = hexstring[10:12],hexstring[12:14]
        bz = bz2+bz1
        Bx = Bits(hex=bx).int
        By = Bits(hex=by).int
        Bz = Bits(hex=bz).int
        B = np.array([Bx,By,Bz])
        return B
def readSensor(serial): 
    try:
        # request data   21 
        serial.flushInput()
        string = "5A E8 5A DF 5A CB" #Long range - Fast mode - Start periodic readout
        
        cmd_bytes = bytearray.fromhex(string)
        
        ser.write(cmd_bytes)
        
        msg_b = serial.read(8)
        encoded = str(base64.b16encode(msg_b))
        encoded = encoded.replace("b'","")
        encoded = encoded.replace("'","")
        B = read_hex(encoded)
        #print(B)
        return B

    except (Exception,KeyboardInterrupt) as e:
        print('sensor communication broke down')
        print(str(e))
        serial.flushInput()
        time.sleep(0.2)
        serial.flushOutput()
        time.sleep(0.2)
        
        serial.close() # Only executes once the loop exits
        sys.exit()



def getXMCserialConnection(): 
    # returns serial port object
    # opens the serial port to communicate with the XMC
    global ser
    ports = list(serial.tools.list_ports.comports())
    if (len(ports) != 0):
        for p in ports:
            if ((p.pid == 261) & (p.vid == 4966)): # pid and vid from xmc
                print("XMC found on port: " + p.device)
                try:
                    ser = serial.Serial(p.device, 115200)
                    print('Serial Connection Done')
                    return ser
                except Exception:
                    print('Please unplug then plug back the device')
                    print('Serial Connection Done')
    print('ERROR(getSerialConnection) - Cannot Find a device.')
    sys.exit()