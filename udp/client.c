#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <errno.h>

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

void main(int argc, char* argv[])
{
    int sockfd;
    int sockopt = 1;
    struct sockaddr_in address;
    int res;
    char buffer[1024] = {0};

    memset(&address, 0, sizeof(struct sockaddr_in));

    char *addr = "127.0.0.1";
    if (argc >=2) {
        printf("send to address: %s\n", argv[1]);
        addr = argv[1];
    }

    address.sin_addr.s_addr = inet_addr(addr);
    address.sin_family      = AF_INET;
    address.sin_port        = (uint16_t)htons(6785);

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd == -1) {
        printf("Fatal error while creating socket");
        return;
    }
#if 0
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR,
            (char *)&sockopt, sizeof(sockopt));
    maximize_socket_buffer(sockfd, SO_SNDBUF);
#endif
    printf("please input str >");
    gets(buffer);

    int len = sizeof(address);
    res = sendto(sockfd, buffer, strlen(buffer) + 1, 0,
        (struct sockaddr *)&address, len);

    res = recvfrom(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr *)&address, &len);

    buffer[res] = '\0';
    printf("read %d bytes: %s\n", res, buffer);

    close(sockfd);
    return;
}
