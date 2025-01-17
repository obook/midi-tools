#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:52:22 2025
@author: obooklage
Print message to Arturia Keylab 61 Essential's LCD
Original code by 'Couack'
From https://community.gigperformer.com/t/arturia-keylab-display-on-lcd-screen/4942
"""
import platform
import mido

KEYLAB_LCD_PRE = [0x00, 0x20, 0x6B, 0x7F, 0x42, 0x04, 0x00, 0x60, 0x01]
KEYLAB_LCD_SEP = [0x00, 0x02]
KEYLAB_LCD_END = [0x00]


def DevicesList():
    Inputs = []
    Outputs = []
    IOPorts = []

    for i, port_name in enumerate(mido.get_output_names()):
        if platform.system() == "Linux":  # cleanup linux ports
            port_name = port_name[: port_name.rfind(" ")]
        Outputs.append(port_name)

    for i, port_name in enumerate(mido.get_input_names()):
        if platform.system() == "Linux":  # cleanup linux ports
            port_name = port_name[: port_name.rfind(" ")]
        Inputs.append(port_name)

    for i, port_name in enumerate(mido.get_ioport_names()):  # not used
        if platform.system() == "Linux":  # cleanup linux ports
            port_name = port_name[: port_name.rfind(" ")]
        IOPorts.append(port_name)
        
    print("*************** Outputs")
    print(Outputs)

    '''
    print("*************** Inputs")
    print(Inputs)
    '''

    print("*************** IOPorts")
    print(IOPorts)

    
    return Inputs, Outputs, IOPorts

def StringToDec(s):
    dec = []
    for c in s:
        if ord(c) > 127:  # only ASCII please...
            c = " "
        dec.append(int(ord(c)))
        if len(dec) > 15:  # no more 16 chars please...
            break
    return dec


DevicesList()

# Windows :
device_name = "Arturia KeyLab Essential 61 3"

LINE1 = StringToDec("This is the fist line")
LINE2 = StringToDec("And the second line")

msg = mido.Message('sysex', data=[])
msg.data += KEYLAB_LCD_PRE
msg.data += LINE1
msg.data += KEYLAB_LCD_SEP
msg.data += LINE2
msg.data += KEYLAB_LCD_END

# Connect to synth : change here for your device
try:
    device = mido.open_output(device_name)
    device.send(msg)
    device.close()
except Exception as error:
    print("Send to device : ", error)
