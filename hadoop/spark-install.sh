#!/bin/bash

sparkdir=`ls -l /usr/local | grep '^d.*spark.*' | rev | cut -d ' ' -f1 | rev`
ln -s /usr/local/$sparkdir /usr/local/spark

cp /usr/local/spark/conf/spark-env.sh.template /usr/local/spark/conf/spark-env.sh

echo -e "
HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop
JAVA_HOME=/usr/local/jdk
CLASSPATH=$JAVA_HOME/lib
PATH=$PATH:$JAVA_HOME/bin
" >> /usr/local/spark/conf/spark-env.sh

