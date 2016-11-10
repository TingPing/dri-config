# window.py
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

from gettext import gettext as _
from gi.repository import Gio, Gtk

from . import dri

class Window(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(
            default_width=800,
            default_height=400,
            **kwargs
        )
        self.add_dialog = None


        action = Gio.SimpleAction.new('add-application', None)
        self.add_action(action)
        action.connect('activate', self.on_add_application)


        header = Gtk.HeaderBar(show_close_button=True, title=_('DRI Configuration'))
        add_btn = Gtk.Button.new_from_icon_name('list-add-symbolic', Gtk.IconSize.BUTTON)
        add_btn.props.action_name = 'win.add-application'
        header.pack_start(add_btn)
        header.show_all()
        self.set_titlebar(header)

        box = Gtk.Box(Gtk.Orientation.HORIZONTAL)
        sidebar = Gtk.StackSidebar()
        sw = Gtk.ScrolledWindow(child=sidebar, hscrollbar_policy=Gtk.PolicyType.NEVER)
        box.pack_start(sw, False, True, 0)

        stack = Gtk.Stack()
        # Just a basic mockup
        conf = dri.DRIConfig('/etc/drirc')
        device = conf.devices[0]
        for app in device.apps:
            # TODO: Group these by device
            pane = ApplicationPane(app, visible=True)
            stack.add_titled(pane, app.name, app.name)
        sidebar.props.stack = stack

        sw = Gtk.ScrolledWindow(child=stack)
        box.pack_start(sw, True, True, 0)
        box.show_all()
        self.add(box)

    def on_add_application(self, action, param):
        def o(dialog, response):
            self.add_dialog = None

        if not self.add_dialog:
            self.add_dialog = AddDialog(transient_for=self)
            self.add_dialog.connect('delete-event', on_delete)
        self.add_dialog.present()


class AddDialog(Gtk.Dialog):
    def __init__(self, **kwargs):
        super().__init__(
            use_header_bar=True,
            modal=True,
            **kwargs
        )


class OptionEntry(Gtk.ListBoxRow):
    def __init__(self, option, value, **kwargs):
        super().__init__(**kwargs)

        # TODO: Make this modifiable, group them, use friendly descriptions
        # show default options
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lbl = Gtk.Label.new(option)
        box.pack_start(lbl, False, True, 0)
        lbl = Gtk.Label.new(value)
        box.pack_start(lbl, True, True, 0)
        self.add(box)


class OptionList(Gtk.ListBox):
    def __init__(self, options, **kwargs):
        super().__init__(**kwargs)

        for option, value in options.items():
            row = OptionEntry(option, value)
            self.add(row)


class ApplicationPane(Gtk.Box):
    def __init__(self, appinfo, **kwargs):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, **kwargs)

        label = Gtk.Label.new('Executable: {}'.format(appinfo.executable))
        self.pack_start(label, False, True, 0)
        self.pack_start(OptionList(appinfo.options), True, True, 0)
