#!/usr/bin/env python

from gi.repository import Gtk, GdkPixbuf, WebKit
import os, sys
import urllib

UI_FILE = "browser.ui"

class Browser:
  def __init__(self):
    self.builder = Gtk.Builder()
    self.builder.add_from_file(UI_FILE)
    self.builder.connect_signals(self)

    self.back = self.builder.get_object("back")
    self.forward = self.builder.get_object("forward")
    self.url = self.builder.get_object("url")

    self.webview = WebKit.WebView()
    scrolled_window = self.builder.get_object("scrolledwindow")
    scrolled_window.add(self.webview)

    self.webview.connect("title-changed", self.on_title_changed)
    self.webview.connect("icon-loaded", self.on_icon_loaded)
    self.webview.connect("load-started", self.on_load_started)
    self.webview.connect("load-finished", self.on_load_finished)

    self.window = self.builder.get_object("window")
    self.window.show_all()

  def on_button_clicked(self, button):
    if button.get_stock_id() == Gtk.STOCK_GO_FORWARD:
      self.webview.go_forward()
    elif button.get_stock_id() == Gtk.STOCK_GO_BACK:
      self.webview.go_back()

  def on_entry_activate(self, widget):
    url = widget.get_text()
    if not "http://" in url:
      url = "http://" + url
    self.webview.load_uri(url)

  def on_title_changed(self, webview, frame, title):
    self.window.set_title(title)

  def on_icon_loaded(self, webview, url):
    try:
      f = urllib.urlopen(url)
      data = f.read()
      pixbuf_loader = GdkPixbuf.PixbufLoader()
      pixbuf_loader.write(data)
      pixbuf_loader.close()
      pixbuf = pixbuf_loader.get_pixbuf()
      self.url.set_icon_from_pixbuf(Gtk.EntryIconPosition.PRIMARY, pixbuf)
    except:
      self.url.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "applications-internet")

  def on_load_started(self, webview, frame):
    self.url.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "image-loading")

  def on_load_finished(self, webview, frame):
    self.url.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, None)
    self.url.set_text(frame.get_uri())

    if self.webview.can_go_back():
      self.back.set_sensitive(True)
    else:
      self.back.set_sensitive(False)
    if self.webview.can_go_forward():
      self.forward.set_sensitive(True)
    else:
      self.forward.set_sensitive(False)

  def destroy(self, window):
    Gtk.main_quit()

def main():
  app = Browser()
  Gtk.main()

if __name__ == "__main__":
  main()
