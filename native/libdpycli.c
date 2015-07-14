#include "libdpycli.h"

char path[108] = "/tmp/d2";
char startFlag[] = "<$";
char endFlag[] = "$>";

int
dpy_sendto(char cmd[]){
	struct sockaddr_un un;
	memset(&un, 0, sizeof(un));
	un.sun_family = AF_UNIX;
	strcpy(un.sun_path, path);

	int sockfd = socket(AF_UNIX, SOCK_STREAM, 0);
	if(sockfd < 0){
		perror("socket error");
		return -1;
	}
	if(connect(sockfd, (struct sockaddr *)&un, sizeof(un.sun_family) + strlen(un.sun_path))){
		perror("socket error");
		return -1;
	}
	char cmd_[1024] = "";
	sprintf(cmd_, "%s%s%s", startFlag, cmd, endFlag);
	int len = strlen(un.sun_path) + sizeof(un.sun_family);
	int rs = write(sockfd, cmd_, strlen(cmd_));
	if(rs < 0){
		perror("socket error");
		return -1;
	}
	return 0;
}
