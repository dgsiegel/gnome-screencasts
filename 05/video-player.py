#!/usr/bin/env python

from gi.repository import Gtk, Clutter, GtkClutter, ClutterGst
import os, sys

UI_FILE = "video-player.ui"

class VideoPlayer:
  def __init__(self):
    self.builder = Gtk.Builder()
    self.builder.add_from_file(UI_FILE)
    self.builder.connect_signals(self)

    self.progress = self.builder.get_object('progress')
    self.button = self.builder.get_object('button')

    clutter_widget = GtkClutter.Embed()
    clutter_widget.set_size_request(600, 400)

    self.videotexture = ClutterGst.VideoTexture()
    self.videotexture.connect("size-change", self.on_size_change, clutter_widget)
    self.videotexture.connect("notify::progress", self.on_progress_change)
    self.videotexture.connect("eos", self.on_eos)

    stage = clutter_widget.get_stage()
    stage.set_color(Clutter.Color())

    stage.add_actor(self.videotexture)
    stage.show_all()

    box = self.builder.get_object('box')
    box.add(clutter_widget)
    box.reorder_child(clutter_widget, 0)

    self.window = self.builder.get_object('window')
    self.window.show_all()

  def on_button_clicked(self, button):
    if button.get_label() == Gtk.STOCK_MEDIA_PLAY:
      self.videotexture.set_playing(True)
      button.set_label(Gtk.STOCK_MEDIA_PAUSE)
    elif button.get_label() == Gtk.STOCK_MEDIA_PAUSE:
      self.videotexture.set_playing(False)
      button.set_label(Gtk.STOCK_MEDIA_PLAY)
    else:
      dialog = Gtk.FileChooserDialog ("Open Video", button.get_toplevel(), Gtk.FileChooserAction.OPEN)
      dialog.add_button(Gtk.STOCK_CANCEL, 0)
      dialog.add_button(Gtk.STOCK_OPEN, 1)
      dialog.set_default_response(1)

      filefilter = Gtk.FileFilter()
      filefilter.add_mime_type("video/*")
      dialog.set_filter(filefilter)

      if dialog.run() == 1:
        self.videotexture.set_filename(dialog.get_filename())
        self.videotexture.set_playing(True)
        button.set_label(Gtk.STOCK_MEDIA_PAUSE)
        self.progress.set_sensitive(True)
      dialog.destroy()

  def on_size_change(self, texture, width, height, widget):
    widget.set_size_request(width, height)

  def on_progress_change(self, texture, param):
    self.progress.set_value(texture.get_progress() * 100.0)

  def on_value_change(self, widget, direction, position):
    self.videotexture.set_progress(position / 100.0)

  def on_eos(self, texture):
    self.button.set_label(Gtk.STOCK_MEDIA_PLAY)

  def destroy(self, window):
    Gtk.main_quit()

def main():
  GtkClutter.init(sys.argv)
  ClutterGst.init(0, "")
  app = VideoPlayer()
  Gtk.main()

if __name__ == '__main__':
  main()
