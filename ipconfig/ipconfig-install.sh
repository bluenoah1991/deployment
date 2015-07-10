#!/bin/bash

# parameters
# h : ipaddr and hostname array (comma separated)

while getopts 's:' OPT; do
	case $OPT in
		s)
			s=$OPTARG;;
	esac
done

if [ ! $s ]; then
	echo 'parameters not found'
	exit -1
fi

if [ -f /etc/hosts.x ]; then
	echo 'repeat configuration'
	exit 0
fi

cp /etc/hosts /etc/hosts.x

arr=(${s//,/ })

for ((i=0; i<${#arr[@]}; ++i))
do
	if [[ `expr ${i} % 2` == 0 ]]; then
		echo -e "${arr[${i}]}\\t${arr[`expr ${i} + 1`]}" >> /etc/hosts
	fi
done

