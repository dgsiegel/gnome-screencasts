#!/usr/bin/env python

from gi.repository import Gtk

class MyCoolApp:
  def __init__(self):
    window = Gtk.Window()
    window.set_title("My awesome window")
    window.set_default_size(300, 200)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect("destroy", self.destroy)

    button = Gtk.Button("Hit me!")
    button.connect_after("clicked", self.button_clicked)
    window.add(button)

    window.show_all()

  def destroy(self, window):
    Gtk.main_quit()

  def button_clicked(self, button):
    print "Ouch! Don't do that again!!"

def main():
  app = MyCoolApp()
  Gtk.main()

if __name__ == '__main__':
  main()
