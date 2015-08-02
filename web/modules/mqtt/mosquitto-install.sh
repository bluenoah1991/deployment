#!/bin/bash

MOSQUITTO_URL=http://mosquitto.org/files/source/mosquitto-1.4.2.tar.gz
MOSQUITTO_FILENAME=mosquitto-1.4.2.tar.gz

wget ${MOSQUITTO_URL} --output-document=/tmp/${MOSQUITTO_FILENAME}
cd /tmp
tar -xvf ${MOSQUITTO_FILENAME} -C /usr/local

MOSQUITTO_DIR=`ls -l /usr/local | grep mosquitto- | rev | cut -d ' ' -f1 | rev`
echo "*******${MOSQUITTO_DIR}*******"

ln -s /usr/local/${MOSQUITTO_DIR} /usr/local/mosquitto

apt-get update
apt-get install libwebsockets3 -y
apt-get install libwebsockets-dev -y
apt-get install openssl -y
apt-get install libssl-dev build-essential zlibc zlib-bin libidn11-dev libidn11 -y
apt-get install libc-ares-dev -y
apt-get install uuid-dev -y

cp /usr/local/mosquitto/config.mk /usr/local/mosquitto/config.mk.x
sed -i "/^WITH_WEBSOCKETS/cWITH_WEBSOCKETS:=yes" /usr/local/mosquitto/config.mk

cd /usr/local/mosquitto
make
make install

cp /usr/local/mosquitto/mosquitto.conf /usr/local/mosquitto/mosquitto.conf.x
echo -e "
user root

listener 1883

listener 9001 0.0.0.0
protocol websockets
" >> /usr/local/mosquitto/mosquitto.conf

mosquitto -c /usr/local/mosquitto/mosquitto.conf -d

echo 'success!'
