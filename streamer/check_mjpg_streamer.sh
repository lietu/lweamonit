#!/bin/bash

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

# Determine directory for scripts
DIR=$(dirname -- $(readlink -f -- "${0}"))

# Load config
source "$DIR/streamer_config.sh"

# Check if screens are found already
PROCESSES=`screen -list | grep "$SCREEN_NAME" | wc -l`

# If we didn't find any
if [ $PROCESSES -lt 1 ]; then
	# Start screen and the start_mjpg_streamer.sh inside it
	$SCREEN_COMMAND "$DIR/start_mjpg_streamer.sh"

	# Say we needed to start it
	echo "Did not find screen with mjpg_streamer, started one."
fi
