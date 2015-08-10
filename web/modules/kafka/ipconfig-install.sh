#!/bin/bash

# parameters
# h : hostname 
# s : ipaddr and hostname array (comma separated)

while getopts 'h:s:' OPT; do
	case $OPT in
		h)
			h=$OPTARG;;
		s)
			s=$OPTARG;;
	esac
done

if [ ! $h ] || [ ! $s ]; then
	echo 'parameters not found'
	exit -1
fi

if [ -f /etc/hostname.x ]; then
	echo 'repeat configuration'
else
	cp /etc/hostname /etc/hostname.x
	echo $h > /etc/hostname
	hostname $h
fi

if [ -f /etc/hosts.x ]; then
	echo 'repeat configuration'
else
	cp /etc/hosts /etc/hosts.x
	arr=(${s//,/ })
	for ((i=0; i<${#arr[@]}; ++i))
	do
		if [[ `expr ${i} % 2` == 0 ]]; then
			echo -e "${arr[${i}]}\\t${arr[`expr ${i} + 1`]}" >> /etc/hosts
		fi
	done
fi


