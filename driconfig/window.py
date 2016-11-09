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
from gi.repository import Gtk

from . import dri

class Window(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(
            default_width=800,
            default_height=400,
            **kwargs
        )

        header = Gtk.HeaderBar(show_close_button=True, title=_('DRI Configuration'))
        header.pack_start(Gtk.Button.new_from_icon_name('list-add-symbolic', Gtk.IconSize.BUTTON))
        header.show_all()
        self.set_titlebar(header)

        box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        sidebar = Gtk.StackSidebar()
        sw = Gtk.ScrolledWindow(child=sidebar, hscrollbar_policy=Gtk.PolicyType.NEVER)
        box.pack_start(sw, False, True, 0)

        stack = Gtk.Stack()
        # Just a basic mockup
        conf = dri.DRIConfig('/etc/drirc')
        device = conf.devices[0]
        for app in device.apps:
            pane = ApplicationPane(app, visible=True)
            stack.add_titled(pane, app.name, app.name)

        sidebar.set_stack(stack)
        box.show_all()
        self.add(box)


class ApplicationPane(Gtk.Grid):
    def __init__(self, appinfo, **kwargs):
        super().__init__(**kwargs)
