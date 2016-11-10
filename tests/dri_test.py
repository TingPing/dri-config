# dri_test.py
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

import unittest

from driconfig import dri

class DriTests(unittest.TestCase):
    def test_load(self):
        self.conf = dri.DRIConfig('tests/drirc.xml')
        self.assertEqual(len(self.conf.devices), 2)
        self.assertEqual(len(self.conf.devices[0].apps), 3)
        self.assertEqual(len(self.conf.devices[1].apps[0].options), 2)

if __name__ == '__main__':
    unittest.main()
