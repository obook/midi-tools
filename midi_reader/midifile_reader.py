# This Python file uses the following encoding: utf-8

import mido
from midi_numbers import number_to_note


class class_reader:

    filename = None
    list_notes = []

    def __init__(self, filename):
        self.filename = filename

    def get_notes(self):
        # Notes in selected channels (0-15)
        for msg in mido.MidiFile(self.filename):

            if msg.type == "note_on":
                # if msg.channel == 0 and msg.velocity:  # only channel 1
                #  Warning : midi_numbers is 1 based, not zero.
                print(msg, number_to_note(msg.note))  # -12
                self.list_notes.append(msg)
            elif msg.type == "note_off":
                pass

        return self.list_notes

