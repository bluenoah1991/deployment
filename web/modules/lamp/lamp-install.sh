#!/bin/bash

MYSQLPWD=123456

while getopts 'y:' OPT; do
        case $OPT in
                p)
                        MYSQLPWD=$OPTARG;;
        esac
done

apt-get update
apt-get install apache2 -y
echo "ServerName localhost:80" >> /etc/apache2/apache2.conf

debconf-set-selections <<< "mysql-server mysql-server/root_password password ${MYSQLPWD}"
debconf-set-selections <<< "mysql-server mysql-server/root_password_again password ${MYSQLPWD}"
apt-get install mysql-server -y

sudo apt-get install mysql-server libapache2-mod-auth-mysql php5-mysql -y

sudo apt-get install php5 libapache2-mod-php5 php5-mcrypt -y

echo -e "
<?php
phpinfo();
?>
" > /var/www/html/info.php

service apache2 restart
