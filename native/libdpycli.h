#define DLL_PUBLIC __attribute__((visibility("default")))

#include <stdio.h>
#include <sys/un.h>
#include <sys/socket.h>
#include <string.h>

#ifdef __cplusplus
extern "C"
#endif
DLL_PUBLIC
int
dpy_sendto(char []);
