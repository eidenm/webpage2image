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
from optparse import OptionParser

# add security by default (see bugzilla #666280 and #666276)
# enable certificates validation in webkit views unless specified otherwise
session = WebKit.get_default_session()
session.set_property("ssl-use-system-ca-file", True)



class ScreenshotBrowser(Gtk.OffscreenWindow):

    def __init__(self, width, height, user_agent, outputname, outputformat):
        super(ScreenshotBrowser, self).__init__()
        self.init_ui(width, height)
        self.init_output_settings(outputname, outputformat)
        self.init_widgets()
        self.init_settings(width, height, user_agent)
        self.init_signals()

    def init_output_settings(self,outputname,outputformat):
        self.outputname = outputname + "." + outputformat
        self.outputformat = outputformat

    def init_ui(self, width, height):
        self.set_default_size(width, height)
        
    def init_widgets(self):
        box = Gtk.VBox()
        box.show()
        self.add(box)
        # webkit
        self.webview = WebKit.WebView()
        self.webview.show()
        #scroll = Gtk.ScrolledWindow()
        #scroll.add(self.webview)
        scroll.show()
        scroll.get_vscrollbar().set_child_visible(False) 		
        scroll.get_hscrollbar().set_child_visible(False) 		
        box.pack_start(scroll, True, True, 0)
        self.show_all()

    def make_screenshot(self, url):
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
            pixbuf.savev(self.outputname, self.outputformat, [], [])
            Gtk.main_quit()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        uri = sys.argv[1]
    else:
        uri = "http://www.uni-trier.de/"

    usage = "usage: %prog [options] url"
    parser = OptionParser(usage=usage)
    parser = OptionParser()
    parser.add_option('-W', '--width', action='store', type='int', help='Resolution width(default %default)', default="1024")
    parser.add_option('-H', '--height', action='store', type='int', help='Resolution height(default %default)', default="768")
    parser.add_option('-d', '--device', action='store', type='string', help='String of the user-agent (default %default)', default="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36")
    parser.add_option('-o', '--output', action='store', type='string', help='Output-Name without Extension(default %default)', default="output")
    parser.add_option('-f', '--format', action='store', type='string', help='Output-Format(default %default)', default="png")
    (options, args) = parser.parse_args()
	
    browser = ScreenshotBrowser(options.width, options.height, options.device,options.output, options.format)
    browser.make_screenshot(uri)
    browser.show()
    Gtk.main()
