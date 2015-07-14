s = debug

ifeq ($(s), debug)
CXXFLAGS = -g
else
CXXFLAGS = 
endif

all : libdpycli.so

libdpycli.so : libdpycli.c libdpycli.h
	gcc $(CXXFLAGS) -shared -fPIC -fvisibility=hidden -o $@ libdpycli.c

test : test.c libdpycli.so libdpycli.h
	gcc $(CXXFLAGS) -o $@ test.c -L. -ldpycli
