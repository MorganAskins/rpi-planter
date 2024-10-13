#!/bin/bash

function test_internet_connection {
    if ping -c5 8.8.8.8 &> /dev/null
    then
        return 0
    fi
    return 1
}

# If not connected to the internet, reboot
if ! test_internet_connection
then
    echo "No connection. Rebooting."
    echo "$(date): Rebooting due to loss of connection." >> ~/errlog.txt
    reboot
else
    echo "Connection okay."
fi
