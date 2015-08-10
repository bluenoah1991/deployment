#!/bin/bash


while getopts 's:i:' OPT; do
	case $OPT in
		s)
			s=$OPTARG;;
		i)
			i=$OPTARG;;
	esac
done

if [ ! $s ] || [ ! $i ]; then
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

ZooKeeperUrl=http://mirror.bit.edu.cn/apache/zookeeper/stable/zookeeper-3.4.6.tar.gz
ZooKeeperName=zookeeper-3.4.6.tar.gz

wget ${ZooKeeperUrl} --output-document=/tmp/${ZooKeeperName}
tar -zxvf /tmp/${ZooKeeperName} -C /usr/local
lname=`ls -l /usr/local | grep zookeeper- | rev | cut -d ' ' -f1 | rev`
ln -s /usr/local/${lname} /usr/local/zookeeper

cp /usr/local/zookeeper/conf/zoo_sample.cfg /usr/local/zookeeper/conf/zoo.cfg

dataDir='/zookeeper'

sed -i "/^dataDir=/cdataDir=${dataDir}" /usr/local/zookeeper/conf/zoo.cfg
mkdir ${dataDir}

ss=(${s//,/ })
len=${#ss[@]}

for((I=0; I<${len}; ++I))
do
	echo "server.$((I + 1))=${ss[I]}:2888:3888" >> /usr/local/zookeeper/conf/zoo.cfg
done

echo $i > ${dataDir}/myid

/usr/local/zookeeper/bin/zkServer.sh start

echo 'success!'





