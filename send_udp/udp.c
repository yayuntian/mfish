#include "udp.h"



void maximize_socket_buffer(int sock_fd, int buf_type)
{
    int i, rcv_buffsize_base, rcv_buffsize;
    int max_buf_size = 1024 * 200 * 1024  /* 200 MB */, debug = 0;
    socklen_t len = sizeof(rcv_buffsize_base);

    if (getsockopt(sock_fd, SOL_SOCKET, buf_type, &rcv_buffsize_base, &len) < 0) {
        printf("Unable to read socket receiver buffer size [%s]", strerror(errno));
        return;
    } else {
        if (debug) printf("Default socket %s buffer size is %d",
                buf_type == SO_RCVBUF ? "receive" : "send",
                rcv_buffsize_base);
    }

    for (i = 2; ; i++) {
        rcv_buffsize = i * rcv_buffsize_base;
        if (rcv_buffsize > max_buf_size) break;

        if (setsockopt(sock_fd, SOL_SOCKET, buf_type, &rcv_buffsize, sizeof(rcv_buffsize)) < 0) {
            if (debug) printf("Unable to set socket %s buffer size [%s]",
                    buf_type == SO_RCVBUF ? "receive" : "send",
                    strerror(errno));
            break;
        } else if (debug) printf("%s socket buffer size set %d",
                buf_type == SO_RCVBUF ? "Receive" : "Send",
                rcv_buffsize);
    }
}

CollectorAddr collect;
int initUdp(char *addr, uint16_t port)
{
    int sockopt = 1;

#if 0
    struct hostent *hostAddr;
    struct in_addr dstAddr;
    if ((hostAddr = gethostbyname(addr)) == NULL) {
        printf("Unable to resolve address '%s'\n", addr);
        return(-1);
    }
    memcpy(&dstAddr.s_addr, hostAddr->h_addr_list[0], hostAddr->h_length);
#endif
    memset(&collect, 0, sizeof(CollectorAddr));
    collect.addr.sin_addr.s_addr = inet_addr(addr);
    collect.addr.sin_family      = AF_INET;
    collect.addr.sin_port        = (uint16_t)htons(port);


    collect.sockFd = socket(AF_INET, SOCK_DGRAM, 0);
    if (collect.sockFd == -1) {
        printf("Fatal error while creating socket");
        return -1;
    }

    setsockopt(collect.sockFd, SOL_SOCKET, SO_REUSEADDR,
            (char *)&sockopt, sizeof(sockopt));

    maximize_socket_buffer(collect.sockFd, SO_SNDBUF);

    return(0);
}

#if 0
void main()
{
    char* addr = "127.0.0.1";
    uint16_t port = 2055;
    char *str = "just test udp.";

    initUdp(addr, port);

    send_to(collect.sockFd, str, sizeof(*str), 0,
        (struct sockaddr *)&collect->addr, sizeof(collect->addr));
}
#endif
