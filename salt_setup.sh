#!/usr/bin/env bash

if [[ "$UID" != "0" ]]; then
	echo "This script must be run as root."
	exit 1
fi

echo "This script will use Salt Stack to configure this machine for lweamonit."
echo "If this is not what you want to do, press CTRL+C now."
echo
echo "Otherwise, press Enter to continue."

read

# Install Salt
curl --retry 10 -L https://bootstrap.saltstack.com -o install_salt.sh
sh install_salt.sh
rm install_salt.sh

# Configure Salt
mkdir -p /srv
cp -r salt/roots/* /srv
cp salt/minion.conf /etc/salt/

# Tell Salt to configure server
apt-get install -f fonts-dejavu-core
salt-call --local state.highstate

# Activate nginx configuration
service nginx restart
