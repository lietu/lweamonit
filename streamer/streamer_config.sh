#!/bin/bash

CONFIG="$DIR/config.ini"

# Ini parser by Andrés Díaz, from http://ajdiaz.wordpress.com/2008/02/09/bash-ini-parser/

cfg.parser ()
{
    ini="$(<$1)"                # read the file
    ini="${ini//[/\[}"          # escape [
    ini="${ini//]/\]}"          # escape ]
    IFS=$'\n' && ini=( ${ini} ) # convert to line-array
    ini=( ${ini[*]//;*/} )      # remove comments with ;
    ini=( ${ini[*]/\    =/=} )  # remove tabs before =
    ini=( ${ini[*]/=\   /=} )   # remove tabs be =
    ini=( ${ini[*]/\ =\ /=} )   # remove anything with a space around =
    ini=( ${ini[*]/#\\[/\}$'\n'cfg.section.} ) # set section prefix
    ini=( ${ini[*]/%\\]/ \(} )    # convert text2function (1)
    ini=( ${ini[*]/=/=\( } )    # convert item to array
    ini=( ${ini[*]/%/ \)} )     # close array parenthesis
    ini=( ${ini[*]/%\\ \)/ \\} ) # the multiline trick
    ini=( ${ini[*]/%\( \)/\(\) \{} ) # convert text2function (2)
    ini=( ${ini[*]/%\} \)/\}} ) # remove extra parenthesis
    ini[0]="" # remove first element
    ini[${#ini[*]} + 1]='}'    # add the last brace
    eval "$(echo "${ini[*]}")" # eval the result
}

# Read config file 
cfg.parser "$CONFIG"

# Enable MJPG-streamer section
cfg.section.mjpg_streamer

# Read settings we need
MJPG_STREAMER_PATH="$path"
INPUT_DEVICE="$input_device"
IMAGE_RESOLUTION="$resolution"
IMAGE_FPS="$fps"

# Enable screen section of config
cfg.section.screen

# Read settings we need
SCREEN_NAME="$name"


#
# Do some extra variables that can't be parsed from an .ini file
#


# What library to use for mjpg_streamer input
INPUT_LIBRARY="${MJPG_STREAMER_PATH}input_uvc.so"

# Full input options, i.e. -i option parameters for mjpg_streamer
INPUT_OPTIONS="${INPUT_LIBRARY} -d ${INPUT_DEVICE} -r ${IMAGE_RESOLUTION} -f ${IMAGE_FPS}"

# Options for output, defaults to HTTP server at port 8080 with it's www -directory under the mjpg_streamer folder
OUTPUT_OPTIONS="${MJPG_STREAMER_PATH}output_http.so -w ${MJPG_STREAMER_PATH}www"

# Where is screen located?
SCREEN=`which screen`

# Options to execute screen with
SCREEN_PARAMS="-S ${SCREEN_NAME} -d -m";

# Build the full command to run
COMMAND="${MJPG_STREAMER_PATH}mjpg_streamer -i '${INPUT_OPTIONS}' -o '${OUTPUT_OPTIONS}'"
