#!/bin/bash

# parameters
# b : backup
# s : slaves array (comma separated)
# z : zookeepers array (comma spearated)
# h : hdfs path (include dir path)

while getopts 'b:s:z:h:' OPT; do
	case $OPT in
		b)
			b=$OPTARG;;
		s)
			s=$OPTARG;;
		z)
			z=$OPTARG;;
		h)
			h=$OPTARG;;
	esac
done

if [ ! $s ] || [ ! $z ] || [ ! $h ]; then
	echo 'parameters not found'
	exit -1
fi

HBASE_URL=http://mirror.bit.edu.cn/apache/hbase/stable/hbase-1.0.1.1-bin.tar.gz
HBASE_NAME=hbase-1.0.1.1-bin.tar.gz

wget ${HBASE_URL} --output-document=/tmp/${HBASE_NAME}
tar -zxvf /tmp/${HBASE_NAME} -C /usr/local

lname=`ls -l /usr/local | grep hbase- | rev | cut -d ' ' -f1 | rev`
ln -s /usr/local/${lname} /usr/local/hbase

sed -i "/^# export JAVA_HOME=/cexport JAVA_HOME=/usr/local/jdk" /usr/local/hbase/conf/hbase-env.sh
sed -i "/^# export HBASE_MANAGES_ZK=/cexport HBASE_MANAGES_ZK=false" /usr/local/hbase/conf/hbase-env.sh

#if [[ $r == 'master' ]]; then
#
#	ssh-keygen -t rsa -f /tmp/id_rsa -N ''
#	mkdir -p ~/.ssh
#	cp /tmp/id_rsa ~/.ssh/id_rsa
#	chmod 600 ~/.ssh/id_rsa
#	cat /tmp/id_rsa.pub >> ~/.ssh/authorized_keys
#	chmod 600 ~/.ssh/authorized_keys
#	
#
#fi

ss=(${s//,/ })

echo '' > /usr/local/hbase/conf/regionservers
for _ in ${ss[@]}
do
	echo ${_} >> /usr/local/hbase/conf/regionservers
done

if [[ -n ${b} ]]; then

	echo ${b} > /usr/local/hbase/conf/backup-masters

fi

l=`grep -n '<configuration>' /usr/local/hbase/conf/hbase-site.xml | head -1 | cut -d : -f1`
sed -i "${l}a\\
\\t<property>\\
\\t\\t<name>hbase.cluster.distributed</name>\\
\\t\\t<value>true</value>\\
\\t</property>\\
\\t<property>\\
\\t\\t<name>hbase.rootdir</name>\\
\\t\\t<value>${h}</value>\\
\\t</property>\\
\\t<property>\\
\\t\\t<name>hbase.zookeeper.quorum</name>\\
\\t\\t<value>${z}</value>\\
\\t</property>\\
\\t<property>\\
\\t\\t<name>hbase.zookeeper.property.clientPort</name>\\
\\t\\t<value>2181</value>\\
\\t</property>\\
\\t<property>\\
\\t\\t<name>hbase.zookeeper.property.dataDir</name>\\
\\t\\t<value>/zookeeper</value>\\
\\t</property>" /usr/local/hbase/conf/hbase-site.xml


