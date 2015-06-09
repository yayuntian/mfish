#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <errno.h>

typedef struct collectorAddress {
    int sockFd; /* Socket file descriptor */
    uint32_t  flowSeq;
    struct sockaddr_in addr;
} CollectorAddr;

extern CollectorAddr collect;
extern int initUdp(char *addr, uint16_t port);

