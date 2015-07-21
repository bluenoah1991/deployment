#!/bin/bash

if [ -f /etc/profile.x ]; then

	cp /etc/profile.x /etc/profile
	rm /etc/profile.x

fi

