#include <stdio.h> 
#include <stdlib.h>
#include <errno.h>
#include <string.h> 
#include <sys/types.h> 
#include <netinet/in.h> 
#include <sys/socket.h>
#include <arpa/inet.h>

#define SERVPORT 6785
int main() 
{
    int res;
    char buffer[1024];
    int sockfd;
    struct sockaddr_in my_addr;
    struct sockaddr_in remote_addr;
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) == -1) {
        printf("socket creat error\n");
        exit(1); 
    } 
    my_addr.sin_family = AF_INET; 
    my_addr.sin_port = htons(SERVPORT);
    my_addr.sin_addr.s_addr = INADDR_ANY;
    //my_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    //bzero(&(my_addr.sin_zero), 8); 

    if (bind(sockfd, (struct sockaddr *)&my_addr, sizeof(struct sockaddr)) == -1){ 
        printf("bind error\n");
        exit(1);
    }

    int addrlen = sizeof(struct sockaddr_in);
    while (1) {
        res = recvfrom(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr *)&my_addr, &addrlen);
        printf("received a connection from %s \n", inet_ntoa(my_addr.sin_addr));

        buffer[res] = '\0';
        printf("read %d bytes: %s\n", res, buffer);

        res = sendto(sockfd, buffer, res, 0, (struct sockaddr *)&my_addr, addrlen);
    }
    close(sockfd);
} 
