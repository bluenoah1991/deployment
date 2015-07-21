#!/bin/bash

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

