#!/usr/bin/env python3
# setup.py
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

import distutils

distutils.setup(
    name='dri-config',
    version='0.1.0',
    description='A configuration tool for DRI drivers',
    author='Patrick Griffis',
    author_email='tingping@tingping.se',
    license='GPL3+',
    packages=['driconfig'],
    classifiers=['Programming Language :: Python :: 3 :: Only'],
)
