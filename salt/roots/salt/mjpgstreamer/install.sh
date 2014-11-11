#!/usr/bin/env bash

DESTINATION_PATH="/usr/local/bin/mjpg_streamer"

TMP_PATH="/tmp/mjpgstreamer_install"

if [[ ! -d "$DESTINATION_PATH" ]]; then

    # Set up temp directory
    rm -rf "$TMP_PATH"
    mkdir -p "$TMP_PATH"
    cd "$TMP_PATH"

    # Download source
	svn co 'https://svn.code.sf.net/p/mjpg-streamer/code/mjpg-streamer/' mjpg-streamer

	cd mjpg-streamer

	make clean
	make
	make install

	cp *.so /usr/lib

	ldconfig

    # Clean up
    cd
    rm -rf "$TMP_PATH"

    # Report state to Salt
    echo -n "result=True "
    echo -n "comment='Installed mjpg-streamer'"
fi
