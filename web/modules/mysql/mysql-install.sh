#!/bin/bash

MYSQLPWD=123456

while getopts 'p:' OPT; do
        case $OPT in
                p)
                        MYSQLPWD=$OPTARG;;
        esac
done

apt-get update

debconf-set-selections <<< "mysql-server mysql-server/root_password password ${MYSQLPWD}"
debconf-set-selections <<< "mysql-server mysql-server/root_password_again password ${MYSQLPWD}"
apt-get install mysql-server -y

sudo apt-get install mysql-server mysql-client -y

service mysql restart


LINE1="GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'  IDENTIFIED BY '${MYSQLPWD}'  WITH GRANT OPTION;"

mysql -uroot -p${MYSQLPWD} ${DBNAME} << EOF

  ${LINE1}
  FLUSH PRIVILEGES;
  
EOF

service mysql restart
