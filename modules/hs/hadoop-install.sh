#!/bin/bash

# parameters
# m : master hostname
# s : slave hostname array (comma separated)
# t : type (master = 0 and slave = 1)

while getopts 'm:s:t:' OPT; do
	case $OPT in
		m)
			m=$OPTARG;;
		s)
			s=$OPTARG;;
		t)
			t=$OPTARG;;
	esac
done

if [ ! $m ] || [ ! $s ] || [ ! $t ]; then
	echo 'parameters not found'
	exit -1
fi

# x[0]='a'
# x[1]='b'
# x[2]='c'
# for a in ${x[@]}; do
#	echo $a
# done
# echo ${x[1]}

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

hadoopdir=`ls -l /usr/local | grep hadoop- | rev | cut -d ' ' -f1 | rev`
ln -s /usr/local/$hadoopdir /usr/local/hadoop

cfg=/usr/local/hadoop/etc/hadoop

sed -i "1iJAVA_HOME=/usr/local/jdk" ${cfg}/hadoop-env.sh
sed -i "1aHADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop" ${cfg}/hadoop-env.sh

l=`grep -n '<configuration>' ${cfg}/core-site.xml | head -1 | cut -d : -f1`
sed -i "${l}a\\
\\t<property>\\
\\t\\t<name>fs.defaultFS</name>\\
\\t\\t<value>hdfs://${m}:40000</value>\\
\\t</property>" ${cfg}/core-site.xml

l=`grep -n '<configuration>' ${cfg}/hdfs-site.xml | head -1 | cut -d : -f1`
if [[ $t == '0' ]]; then

	sed -i "${l}a\\
\\t<property>\\
\\t\\t<name>dfs.namenode.name.dir</name>\\
\\t\\t<value>/data</value>\\
\\t</property>\\
\\t<property>\\
\\t\\t<name>dfs.hosts</name>\\
\\t\\t<value>/usr/local/hadoop/etc/hadoop/slaves</value>\\
\\t</property>" ${cfg}/hdfs-site.xml

elif [[ $t == '1' ]]; then

	sed -i "${l}a\\
\\t<property>\\
\\t\\t<name>dfs.datanode.data.dir</name>\\
\\t\\t<value>/data</value>\\
\\t</property>" ${cfg}/hdfs-site.xml

fi

l=`grep -n '<configuration>' ${cfg}/yarn-site.xml | head -1 | cut -d : -f1`
sed -i "${l}a\\
\\t<property>\\
\\t\\t<name>yarn.resourcemanager.hostname</name>\\
\\t\\t<value>${m}</value>\\
\\t</property>\\
\\t<property>\\
\\t\\t<name>yarn.nodemanager.vmem-check-enabled</name>\\
\\t\\t<value>false</value>\\
\\t</property>" ${cfg}/yarn-site.xml

if [[ $t == '0' ]]; then

	sed -i "${l}a\\
\\t<property>\\
\\t\\t<name>yarn.resourcemanager.nodes.include-path</name>\\
\\t\\t<value>/usr/local/hadoop/etc/hadoop/slaves</value>\\
\\t</property>" ${cfg}/yarn-site.xml

	echo '' > /usr/local/hadoop/etc/hadoop/slaves
	for _ in ${ss[@]}
	do
		echo ${_} >> /usr/local/hadoop/etc/hadoop/slaves
	done

fi





