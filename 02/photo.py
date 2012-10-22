#!/usr/bin/env python

from gi.repository import Gtk
import os
import sys

class PhotoApp:
  def __init__(self):
    window = Gtk.Window()
    window.set_title("My awesome photo app")
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect("destroy", self.destroy)

    vbox = Gtk.Box()
    vbox.set_spacing(5)
    vbox.set_orientation(Gtk.Orientation.VERTICAL)
    window.add(vbox)

    self.directory = "photos"
    self.photos = os.listdir(self.directory)
    self.photos.sort()
    self.position = 0

    self.image = Gtk.Image()
    self.image.set_from_file(os.path.join(self.directory, self.photos[0]))
    vbox.add(self.image)

    hbox = Gtk.Box(homogeneous=True)
    hbox.set_spacing(5)
    hbox.set_orientation(Gtk.Orientation.HORIZONTAL)
    vbox.add(hbox)

    previous = Gtk.Button.new_from_stock("gtk-media-previous")
    previous.connect_after("clicked", self.change_photo, -1)

    next = Gtk.Button.new_from_stock("gtk-media-next")
    next.connect_after("clicked", self.change_photo, 1)

    hbox.add(previous)
    hbox.add(next)

    window.show_all()

  def change_photo(self, button, direction):
    self.position = (self.position + direction) % len(self.photos)
    self.image.set_from_file(os.path.join(self.directory, self.photos[self.position]))

  def destroy(self, window):
    Gtk.main_quit()

def main():
  app = PhotoApp()
  Gtk.main()

if __name__ == '__main__':
  main()
