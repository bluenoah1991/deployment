#!/bin/bash

# parameters
# h : hostname array (comma separated)
# t : type (master = 0 and slave = 1)

while getopts 'h:t:' OPT; do
	case $OPT in
		h)
			h=$OPTARG;;
		t)
			t=$OPTARG;;
	esac
done

if [ ! $h ] || [ ! $t ]; then
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

num=1

# echo $h
# echo `echo $h | cut -d , -f2`
# if [[ -n `echo $h | cut -d , -f2` ]]; then
# 	echo "ok"
# fi

if [[ `echo $h | cut -d , -f1` == `echo $h | cut -d , -f2` ]]; then
	echo 'parameters exception'
	exit -1
fi

while [[ -n `echo $h | cut -d , -f$num` ]]; do
	hosts[`expr $num - 1`]=`echo $h | cut -d , -f$num`
	num=`expr $num + 1`
done

num=`expr $num - 1`

javadir=`ls -l /usr/local | grep jdk[^-] | rev | cut -d ' ' -f1 | rev`
ln -s /usr/local/$javadir /usr/local/jdk

cp /etc/profile /etc/profile.raw

echo -e "
export JAVA_HOME=/usr/local/jdk
export CLASSPATH=\$JAVA_HOME/lib
export PATH=\$PATH:\$JAVA_HOME/bin
" >> /etc/profile

export JAVA_HOME=/usr/local/jdk
export CLASSPATH=$JAVA_HOME/lib
export PATH=$PATH:$JAVA_HOME/bin

hadoopdir=`ls -l /usr/local | grep hadoop- | rev | cut -d ' ' -f1 | rev`
ln -s /usr/local/$hadoopdir /usr/local/hadoop

cfg=/usr/local/hadoop/etc/hadoop

l=`grep -n '<configuration>' ${cfg}/core-site.xml | head -1 | cut -d : -f1`
sed -i "${l}a\\
\\t<property>\\
\\t\\t<name>fs.defaultFS</name>\\
\\t\\t<value>${hosts[0]}</value>\\
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
\\t\\t<value>${hosts[0]}</value>\\
\\t</property>" ${cfg}/yarn-site.xml

if [[ $t == '0' ]]; then

	sed -i "${l}a\\
\\t<property>\\
\\t\\t<name>yarn.resourcemanager.nodes.include-path</name>\\
\\t\\t<value>/usr/local/hadoop/etc/hadoop/slaves</value>\\
\\t</property>" ${cfg}/yarn-site.xml

fi




