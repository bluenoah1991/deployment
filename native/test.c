#include "libdpycli.h"

int
main(void){

char msg[] = "hello 123";
int rs = dpy_sendto(msg);

return 0;

}
