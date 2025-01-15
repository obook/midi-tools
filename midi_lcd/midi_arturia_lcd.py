#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:52:22 2025
@author: obooklage
Print message to Arturia Keylab 61 Essential's LCD
Original code by 'Couack'
From https://community.gigperformer.com/t/arturia-keylab-display-on-lcd-screen/4942
"""
import mido

KEYLAB_LCD_PRE = [0x00, 0x20, 0x6B, 0x7F, 0x42, 0x04, 0x00, 0x60, 0x01]
KEYLAB_LCD_SEP = [0x00, 0x02]
KEYLAB_LCD_END = [0x00]


def StringToDec(s):
    dec = []
    for c in s:
        dec.append(int(ord(c)))
        if len(dec) > 15:  # no more 16 chars please...
            break
    return dec


LINE1 = StringToDec("Ballade No. 4 in F Minor, Op. 52.mid")
LINE2 = StringToDec("CHOPIN FREDERIC")

msg = mido.Message('sysex', data=[])
msg.data += KEYLAB_LCD_PRE
msg.data += LINE1
msg.data += KEYLAB_LCD_SEP
msg.data += LINE2
msg.data += KEYLAB_LCD_END

# Connect to synth : change here for your device
device = mido.open_output("Arturia KeyLab Essential 61:Arturia KeyLab Essential 61 DAW")
device.send(msg)
device.close()
