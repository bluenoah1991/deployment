# Installation Guide

> 前置条件  

	apt-get install python-pip
	apt-get install python-dev
	pip install paramiko  

> 安装步骤  

	git clone https://github.com/codemeow5/deployment.git
	cd <DEPLOYMENT_ROOT_DIR>/hadoop
	cp jdk-8u45-linux-x64.tar.gz .
	cp hadoop-2.6.0.tar.gz .
	python install.py