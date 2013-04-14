#!/usr/bin/env bash

# Lweamonit - Lightweight weather monitoring station tools
# Copyright (C) 2013  Janne Enberg

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

APPPATH=$(dirname -- $(readlink -f -- "${0}"))

PYTHON=$(which python || which python27)
if [ ! -f "${PYTHON}" ]; then
	echo "Could not find path to the Python executable"
	echo "Please install Python or reconfigure this script (${0})."
	exit 1
fi

"$PYTHON" -m "lweamonit.main"
