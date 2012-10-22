#!/usr/bin/env python

from gi.repository import Gtk

def main():
  window = Gtk.Window()
  window.set_title("My awesome window")
  window.set_default_size(300, 200)
  window.set_position(Gtk.WindowPosition.CENTER)
  window.connect("destroy", destroy)

  button = Gtk.Button("Hit me!")
  button.connect_after("clicked", button_clicked)
  window.add(button)

  window.show_all()
  Gtk.main()

def destroy(window):
  Gtk.main_quit()

def button_clicked(button):
  print "Ouch! Don't do that again!!"

if __name__ == '__main__':
  main()
