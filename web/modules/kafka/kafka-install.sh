#!/bin/bash

KafkaUrl=http://mirror.bit.edu.cn/apache/kafka/0.8.2.0/kafka_2.10-0.8.2.0.tgz
KafkaName=kafka_2.10-0.8.2.0.tgz

wget ${KafkaUrl} --output-document=/tmp/${KafkaName}
tar -zxvf /tmp/${KafkaName} -C /usr/local
lname=`ls -l /usr/local | grep kafka_ | rev | cut -d ' ' -f1 | rev`
ln -s /usr/local/${lname} /usr/local/kafka

sed -i "/^zookeeper.connect=/czookeeper.connect=0.0.0.0:2181" /usr/local/kafka/config/server.properties

export JAVA_HOME=/usr/local/jdk
export CLASSPATH=$JAVA_HOME/lib
export PATH=$PATH:$JAVA_HOME/bin

setsid /usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties &

echo "success!"
