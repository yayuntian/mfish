#include <stdio.h> 
#include <stdlib.h>
#include <errno.h>
#include<unistd.h>
#include <string.h> 
#include <sys/types.h> 
#include <netinet/in.h> 
#include <sys/socket.h>
#include <arpa/inet.h>
#include <signal.h>


#define SERVPORT 6785
uint64_t pkt_count = 0;
uint64_t byt_count = 0;


void hex_printf(unsigned char *str, int len)
{

    int times = len / 16;
    int last = len % 16;
    unsigned char *p = str;
    int i = 0;
    for(i = 0; i < times; i++) {
        printf("<%d>data:0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x\t 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x\n", i,
            p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[13], p[14], p[15]);
        p += 16;
    }   
    printf("<1>Remained %d data have been shown\n",last);

}

void show(int sig)
{
	printf("Recived packet: %ld, bytes: %ld\n", pkt_count, byt_count);
	exit(0);
}

int main(int argc, char **argv)
{
    int res, i;
    unsigned char buffer[8192];
    int sockfd;
	uint16_t port = 6785;
    struct sockaddr_in my_addr;

	signal(SIGINT, show);

	for( i = 1; i< argc; i++) {
        if(strcmp(argv[i],"-p") == 0) {
            port = atoi(argv[i+1]);
            continue;
        }
    }
	
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) == -1) {
        printf("socket creat error\n");
        exit(1); 
    }
	
    my_addr.sin_family = AF_INET; 
    my_addr.sin_port = htons(port);
    my_addr.sin_addr.s_addr = INADDR_ANY;
    //my_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    //bzero(&(my_addr.sin_zero), 8);
    if (bind(sockfd, (struct sockaddr *)&my_addr, sizeof(struct sockaddr)) == -1){ 
        printf("bind error\n");
        exit(1);
    }
	printf("server start, bind port: %d\n", port);
    socklen_t addrlen = sizeof(struct sockaddr_in);
	
    while (1) {
        res = recvfrom(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr *)&my_addr, &addrlen);
        //printf("received a connection from %s \n", inet_ntoa(my_addr.sin_addr));

        //buffer[res] = '\0';
        //printf("read %d bytes:\n", res);
		//hex_printf(buffer, res);
		memset(buffer, 0x00, sizeof(buffer));
		pkt_count++;
		byt_count += res;

        //res = sendto(sockfd, buffer, res, 0, (struct sockaddr *)&my_addr, addrlen);
    }
    close(sockfd);
} 
