#!/usr/bin/env python

from gi.repository import Gtk, Gst, GObject
import os, sys

UI_FILE = "guitar.ui"

class GuitarTuner:
  LENGTH = 500

  frequencies = {
    'E': 329.63,
    'A': 440,
    'D': 587.33,
    'G': 783.99,
    'B': 987.77,
    'e': 1318.51,
  }

  def __init__(self):
    self.builder = Gtk.Builder()
    self.builder.add_from_file(UI_FILE)
    self.builder.connect_signals(self)

    self.pipeline = Gst.Pipeline(name='tuner')
    self.source = Gst.ElementFactory.make('audiotestsrc', 'src')
    sink = Gst.ElementFactory.make('autoaudiosink', 'output')

    self.pipeline.add(self.source)
    self.pipeline.add(sink)

    self.source.link(sink)

    window = self.builder.get_object('window')
    window.show_all()

  def on_button_clicked(self, button):
    self.play_sound(self.frequencies[button.get_label()])

  def stop_sound(self):
    self.pipeline.set_state(Gst.State.NULL)
    return False

  def play_sound(self, frequency):
    self.source.set_property('freq', frequency)

    self.pipeline.set_state(Gst.State.PLAYING)

    GObject.timeout_add(self.LENGTH, self.stop_sound)

  def destroy(self, window):
    Gtk.main_quit()

def main():
  Gst.init(sys.argv)
  app = GuitarTuner()
  Gtk.main()

if __name__ == '__main__':
  main()
