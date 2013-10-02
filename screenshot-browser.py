#!/usr/bin/python
#
# use webkit & GtkOffscreenWindows to create screenshots of a page at
# different resolutions
#
# (c) 2013 Michael Vogt <mvo@debian.org>
#

import sys

from gi.repository import (
    Gtk,
    WebKit,
)

# add security by default (see bugzilla #666280 and #666276)
# enable certificates validation in webkit views unless specified otherwise
session = WebKit.get_default_session()
session.set_property("ssl-use-system-ca-file", True)



class ScreenshotBrowser(Gtk.OffscreenWindow):

    def __init__(self, width, height, user_agent):
        super(ScreenshotBrowser, self).__init__()
        self.init_ui(width, height)
        self.init_widgets()
        self.init_settings(width, height, user_agent)
        self.init_signals()

    def init_ui(self, width, height):
        self.set_default_size(width, height)
        
    def init_widgets(self):
        box = Gtk.VBox()
        box.show()
        self.add(box)
        # webkit
        self.webview = WebKit.WebView()
        self.webview.show()
        scroll = Gtk.ScrolledWindow()
        scroll.add(self.webview)
        scroll.show()
        box.pack_start(scroll, True, True, 0)
        self.show_all()

    def make_screenshot(self, url, target_filename):
        self.webview.load_uri(uri)

    def init_signals(self):
        self.connect("destroy", Gtk.main_quit)
        self.webview.connect("load-progress-changed", self._on_load_changed)

    def init_settings(self, width, height, user_agent):
        settings = self.webview.get_settings()
        settings.set_property("enable-plugins", False)
        settings.set_property("enable-java-applet", False)
        settings.set_property("user-agent", user_agent)
        #attributes = self.webview.get_viewport_attributes()
        #attributes.set_property("device-height", width)
        #attributes.set_property("device-width", height)
        #attributes.set_property("available-height", width)
        #attributes.set_property("available-width", height)

    def _on_load_changed(self, view, percent):
        if percent == 100:
            pixbuf = self.get_pixbuf()
            pixbuf.savev("foo.png", "png", [], [])
            Gtk.main_quit()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        uri = sys.argv[1]
    else:
        uri = "http://www.uni-trier.de/"

    width = 640
    height = 400
    user_agent = "Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"

    browser = ScreenshotBrowser(width, height, user_agent)
    browser.make_screenshot(uri, "foo.png")
    browser.show()
    Gtk.main()
