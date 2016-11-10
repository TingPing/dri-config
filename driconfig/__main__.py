# __main__.py
#
# Copyright (C) 2016 Patrick Griffis <tingping@tingping.se>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import signal
from gettext import gettext as _

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk

from .window import Window
from .about import AboutDialog

class Application(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(application_id='se.tingping.DriConfig',
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                         **kwargs)
        self.window = None
        self.dialog = None

        self.add_main_option('version', ord('v'), GLib.OptionFlags.NONE, GLib.OptionArg.NONE,
                             _('Print the version'), None)

    def do_startup(self):
        Gtk.Application.do_startup(self)
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        action = Gio.SimpleAction.new('about', None)
        action.connect('activate', self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new('quit', None)
        action.connect('activate', self.on_quit)
        self.add_action(action)
        self.add_accelerator('<Primary>q', 'app.quit')

        app_menu = Gio.Menu.new()
        app_menu.append(_('About'), 'app.about')
        app_menu.append(_('Quit'), 'app.quit')
        self.set_app_menu(app_menu)

    def do_command_line(self, command_line) -> int:
        options = command_line.get_options_dict()

        if options.contains('version'):
            # Broken bindings...
            type(command_line).do_print_literal(command_line, '{}\n'.format('0.1.0'))
            return 0

        self.do_activate()
        return 0

    def do_activate(self):
        if not self.window:
            self.window = Window(application=self)
        self.window.present()

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)
        if self.window:
            self.window.destroy()

    def on_about(self, action, param):
        if not self.dialog:
            self.dialog = AboutDialog(transient_for=self.window)
        self.dialog.present()

    def on_quit(self, action, param):
        self.window.destroy()

if __name__ == '__main__':
    app = Application()
    sys.exit(app.run())
