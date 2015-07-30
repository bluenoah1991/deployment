#!/bin/bash

if [ -f /etc/profile.x ]; then

	cp /etc/profile.x /etc/profile
	rm /etc/profile.x

fi

if [ -f /etc/sysctl.conf.x ]; then

	cp /etc/sysctl.conf.x /etc/sysctl.conf
	rm /etc/sysctl.conf.x

fi
