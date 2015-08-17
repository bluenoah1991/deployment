#!/bin/bash

# parameters
# m : master hostname 
# t : type (master = 0 and slave = 1)

while getopts 'm:t:' OPT; do
	case $OPT in
		m)
			m=$OPTARG;;
		t)
			t=$OPTARG;;
	esac
done

if [ ! $m ] || [ ! $t ]; then
	echo 'parameters not found'
	exit -1
fi

if [ ! -f /etc/sysctl.conf.x ]; then

	cp /etc/sysctl.conf /etc/sysctl.conf.x

	echo -e "
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
" >> /etc/sysctl.conf

sysctl -p /etc/sysctl.conf

fi

ss=(${s//,/ })

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

apt-get update 
apt-get install make g++ -y
MESOS_URL=http://www.apache.org/dist/mesos/0.23.0/mesos-0.23.0.tar.gz
MESOS_NAME=mesos-0.23.0.tar.gz
wget ${MESOS_URL} --output-document=/tmp/${MESOS_NAME}
tar -zxvf /tmp/${MESOS_NAME} -C /tmp

apt-get -y install build-essential python-dev python-boto 
apt-get -y install libcurl4-nss-dev libsasl2-dev maven libapr1-dev libsvn-dev

mkdir /usr/local/mesos
cd /usr/local/mesos
# srcdir=`ls -l /tmp | grep mesos- | rev | cut -d ' ' -f1 | rev`
ln -s /tmp/mesos-0.23.0 /tmp/mesos
/tmp/mesos/configure
make
make install

if [[ $t == '0' ]]; then
	mkdir /usr/local/mesos/workdir
	setsid ./bin/mesos-master.sh --ip=0.0.0.0 --work_dir=/usr/local/mesos/workdir &
else
	setsid ./bin/mesos-slave.sh --master=${m}:5050
fi

echo "success!"

