#!/usr/bin/env python

from gi.repository import Gtk, Pango, Gdk

class Calculator:
  def __init__(self):
    window = Gtk.Window()
    window.set_title("Calculator")
    window.set_position(Gtk.WindowPosition.CENTER)
    window.set_default_size(300, 300)
    window.set_icon_name("accessories-calculator")
    window.connect("destroy", self.destroy)

    window.connect("key-press-event", self.key_pressed)

    box_main = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
    window.add(box_main)

    self.entry = Gtk.Entry()
    self.entry.set_alignment(1)
    self.entry.set_size_request(-1, 50)
    self.entry.set_can_focus(False)

    font_description = self.entry.get_style().font_desc
    font_description.set_absolute_size(24 * Pango.SCALE)
    self.entry.modify_font(font_description)

    box_main.add(self.entry)

    buttons = [7, 8, 9, "/",
               4, 5, 6, "*",
               1, 2, 3, "-",
               0, "C", "=", "+"]

    for i in range(4):
      hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
      hbox.set_homogeneous(True)
      box_main.pack_start(hbox, True, True, 0)
      for j in range(4):
        button = Gtk.Button(buttons[i * 4 + j])
        button.connect_after("clicked", self.button_clicked)
        button.set_can_focus(False)
        hbox.add(button)

    window.show_all()

  def button_clicked(self, button):
    self.calculate(button.get_label())

  def key_pressed(self, widget, event):
    keys = {
            Gdk.KEY_0: 0, Gdk.KEY_KP_0: 0,
            Gdk.KEY_1: 1, Gdk.KEY_KP_1: 1,
            Gdk.KEY_2: 2, Gdk.KEY_KP_2: 2,
            Gdk.KEY_3: 3, Gdk.KEY_KP_3: 3,
            Gdk.KEY_4: 4, Gdk.KEY_KP_4: 4,
            Gdk.KEY_5: 5, Gdk.KEY_KP_5: 5,
            Gdk.KEY_6: 6, Gdk.KEY_KP_6: 6,
            Gdk.KEY_7: 7, Gdk.KEY_KP_7: 7,
            Gdk.KEY_8: 8, Gdk.KEY_KP_8: 8,
            Gdk.KEY_9: 9, Gdk.KEY_KP_9: 9,
            Gdk.KEY_slash: "/", Gdk.KEY_KP_Divide: "/",
            Gdk.KEY_asterisk: "*", Gdk.KEY_KP_Multiply: "*",
            Gdk.KEY_plus: "+", Gdk.KEY_KP_Add: "+",
            Gdk.KEY_minus: "-", Gdk.KEY_KP_Subtract: "-",
            Gdk.KEY_c: "C", Gdk.KEY_C: "C",
            Gdk.KEY_Return: "=", Gdk.KEY_KP_Enter: "=",
           }
    if keys.has_key(event.keyval):
      self.calculate(keys[event.keyval])

  def calculate(self, item):
    if item == "=":
      try:
        value = repr(eval(str(self.entry.get_text())))
        if value == "42":
          self.entry.set_text("i love ice cream")
          return
      except:
        self.entry.override_color(Gtk.StateType.NORMAL, Gdk.RGBA(red=1.0, green=0, blue=0))
      self.entry.set_text(value)
    elif item == "C":
      self.entry.override_color(Gtk.StateType.NORMAL, None)
      self.entry.set_text("")
    else:
      self.entry.override_color(Gtk.StateType.NORMAL, None)
      self.entry.insert_text(str(item), -1)

  def destroy(self, window):
    Gtk.main_quit()

def main():
  app = Calculator()
  Gtk.main()

if __name__ == '__main__':
  main()
