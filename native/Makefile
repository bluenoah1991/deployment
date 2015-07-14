all : libdpycli.so

libdpycli.so : libdpycli.c libdpycli.h
	gcc -shared -fPIC -fvisibility=hidden -o $@ libdpycli.c
