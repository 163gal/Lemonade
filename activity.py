#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2007-8 One Laptop per Child Association, Inc.
# Written by C. Scott Ananian <cscott@laptop.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""Activity helper classes."""
from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox

# Set to false to hide terminal and auto quit on exit
DEBUG_TERMINAL = False


class VteActivity(activity.Activity):
    """Activity subclass built around the Vte terminal widget."""

    def __init__(self, handle):
        from gi.repository import Gtk
        from gi.repository import Gdk
        from gi.repository import GLib
        from gi.repository import Pango
        from gi.repository import Vte

        super(VteActivity, self).__init__(handle, create_jobject=False)
        self.__source_object_id = None

        # creates vte widget
        self._vte = Vte.Terminal()

        if DEBUG_TERMINAL:
            toolbox = ToolbarBox(self)
            toolbar = toolbox.toolbar
            self.set_toolbar_box(toolbox)

            self._vte.set_size(30, 5)
            self._vte.set_size_request(200, 300)
            font = 'Monospace 10'
            self._vte.set_font(Pango.FontDescription(font))
            self._vte.set_colors(Gdk.color_parse('#E7E7E7'),
                                 Gdk.color_parse('#000000'),
                                 [])

            vtebox = Gtk.HBox()
            vtebox.pack_start(self._vte, True, True, 0)
            vtesb = Gtk.VScrollbar()
            vtebox.pack_start(vtesb, False, False, 0)
            self.set_canvas(vtebox)

            toolbox.show_all()
            vtebox.show_all()

        # now start subprocess.
        self._vte.connect('child-exited', self.on_child_exit)
        self._vte.grab_focus()
        bundle_path = activity.get_bundle_path()
        self._pid = self._vte.spawn_sync(
            Vte.PtyFlags.DEFAULT, bundle_path, [
                '/bin/sh', '-c', 'python %s/LemonadeStand.py --width=1200 --height=900 --font=36' %
                bundle_path], [
                "PYTHONPATH=%s/library" %
                bundle_path], GLib.SpawnFlags.DO_NOT_REAP_CHILD, None, None)

    def on_child_exit(self, widget, status):
        """This method is invoked when the user's script exits."""
        if not DEBUG_TERMINAL:
            import sys
            sys.exit()
