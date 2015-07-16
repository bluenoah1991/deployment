#!/bin/bash

if [ -f /etc/hosts.x ]; then

	cp /etc/hosts.x /etc/hosts
	rm /etc/hosts.x

fi

