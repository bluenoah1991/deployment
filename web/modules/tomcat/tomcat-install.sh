#!/bin/bash

if [ ! -f /etc/sysctl.conf.x ]; then

	cp /etc/sysctl.conf /etc/sysctl.conf.x

	echo -e "
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
" >> /etc/sysctl.conf

sysctl -p /etc/sysctl.conf

fi

javadir=`ls -l /usr/local | grep jdk[^-] | rev | cut -d ' ' -f1 | rev`
ln -s /usr/local/$javadir /usr/local/jdk


if [ ! -f /etc/profile.x ]; then

	cp /etc/profile /etc/profile.x
	
	echo -e "
export JAVA_HOME=/usr/local/jdk
export CLASSPATH=\$JAVA_HOME/lib
export PATH=\$PATH:\$JAVA_HOME/bin
" >> /etc/profile

fi

export JAVA_HOME=/usr/local/jdk
export CLASSPATH=$JAVA_HOME/lib
export PATH=$PATH:$JAVA_HOME/bin

apt-get install tomcat7 -y

