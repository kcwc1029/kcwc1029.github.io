#!/bin/bash

/sbin/ifconfig | grep "inet addr:" | awk '{print $2}' | cut -f2 -d:

echo

/sbin/ifconfig | grep "inet addr:" | awk '{print $2}' | cut -f2 -d: | head -1