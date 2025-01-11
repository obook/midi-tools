#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 22:49:02 2025

@author: obooklage

pip install JACK-Client

"""

import sys
import jack
import binascii

try:
    client = jack.Client('MyPythonJackClient', no_start_server=True)
except jack.JackError as exc:
    print("Could not create JACK client::", exc)
    sys.exit()

if client.status.server_started:
    print('JACK server was started')
else:
    print('JACK server was already running')

audio_input = client.inports.register('jack input')
audio_output = client.outports.register('jack output')

midi_input = client.midi_inports.register('jack midi_in')
midi_output = client.midi_outports.register('jack midi_output')


@client.set_process_callback
def process(frames):
    for offset, data in midi_input.incoming_midi_events():
        print('{}: 0x{}'.format(client.last_frame_time + offset,
                                binascii.hexlify(data).decode()))


@client.set_port_connect_callback
def port_connect(a, b, connect):
    print(['disconnected', 'connected'][connect], a, 'and', b)


@client.set_xrun_callback
def xrun(delay):
    print('xrun; delay', delay, 'microseconds')


with client:
    print('#' * 80)
    print('press Return to quit')
    print('#' * 80)
    input()

client.deactivate()
client.close()
