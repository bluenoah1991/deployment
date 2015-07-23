#!/bin/bash

if [ -f /etc/hostname.x ]; then
	cp /etc/hostname.x /etc/hostname
	rm /etc/hostname.x
fi

if [ -f /etc/hosts.x ]; then
	cp /etc/hosts.x /etc/hosts
	rm /etc/hosts.x
fi

