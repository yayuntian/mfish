#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif
#define __USE_GNU

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <sched.h>
#include <unistd.h>
#include <assert.h>
#include <errno.h>
#include <string.h>
#include <fcntl.h>
#include <sys/time.h>
#include <time.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <pthread.h>
#include <signal.h>

#include "pkt_buff.h"
#include "udp.h"

#include <linux/if_ether.h>
#include <linux/ip.h>                                                                                
#include <linux/udp.h>
#include <linux/tcp.h>


int over_sized_packets  = 0;
int total_files_num = 0;
static pthread_t  open_file_ctrl;

int iter_num;

int mybind_cpu(int core)
{
    int ret ;
    cpu_set_t mask;

    CPU_ZERO(&mask);
    CPU_SET(core, &mask);

    ret = sched_setaffinity(0, sizeof(cpu_set_t), &mask);

    assert(ret >= 0);

    return ret;
}

#define LIMIT_SPEED 1
volatile int speed_loop = 0;
#define IO_BATCH_SIZE 64

static uint64_t pkt_count = 0;
static uint64_t pkt_bytes = 0;


void show(int sig)
{
	printf("Send packet: %ld, bytes: %ld\n", pkt_count, pkt_bytes);
	exit(0);
}


int send_to(u_char *pktdata, uint32_t pktlen)
{
    int res;
    time_t timep;

    res = sendto(collect.sockFd, pktdata, pktlen, 0,
            (struct sockaddr *)&collect.addr, sizeof(collect.addr));

    time(&timep);
	pkt_bytes += res;
    if((pkt_count++ & 0xffff) == 0x01)
        printf("pkt_count %ld, bytes: %ld ----%s", pkt_count, pkt_bytes, ctime(&timep));

    return res;
}

#if USE_BUF

#define BUF_MAX	4096
static u_char buffer[BUF_MAX] = {0};
static uint32_t buf_len = 0;

#endif
void echo(int b_index)
{
    file_cache_t *fct;
    u_char *pktdata;
    uint32_t pktlen;
    uint32_t offset;
    uint32_t datalen;

    //struct ethhdr *eth;
    struct iphdr *ip;
    //struct udphdr *udp;
    struct tcphdr *tcp;
    u_char *payload;


    fct  = (file_cache_t *) &fifo_pcap_cache[b_index].pcap_cache_trace;

    while(1) {
        pktdata = prep_next_skb(fct, &pktlen, b_index);
        if (!pktdata) {
            goto end_of_trace;
        }

		//eth = (struct ethhdr*) pktdata;
		ip = (struct iphdr *)(pktdata + sizeof(struct ethhdr));
        int iplen = ntohs(ip->tot_len);
        switch (ip->protocol) {
            case 6: //tcp
		        tcp = (struct tcphdr *)((char *)ip + 4 * ip->ihl);
                offset = 4 * ip->ihl + 4 * tcp->doff;
                datalen = iplen - offset;
                break;
            case 17:    //udp
		        //udp = (struct udphdr *)((char *)ip + 4 * ip->ihl);
                offset = 4 * ip->ihl + sizeof(struct udphdr);
                datalen = iplen - offset;
                break; 
            default: 
                continue;
        }
		if (datalen == 0) continue;

        if (pktlen != datalen + sizeof(struct ethhdr) + offset){
            printf("error pktlen: %d, data: %ld\n", pktlen, datalen + sizeof(struct ethhdr) + offset);
            exit(0);
        }
        payload = pktdata + sizeof(struct ethhdr) + offset;

		send_to(payload, datalen);

#if USE_BUF
		if (buf_len + datalen < BUF_MAX) {
			memcpy(buffer, payload, datalen);
			buf_len += datalen;
			continue;
		}
        send_to(buffer, buf_len);

		buf_len = 0;
		memset(buffer, 0, sizeof(buffer));
#endif
		
    }
end_of_trace:
    //printf("*************^^^^^^^^^^^^^************\n");
    release_pkt_buff(b_index);
}

#define PRINT_LIMIT (1024*1024*1024)
int sending_packets(int ifindex)
{
    int      i, ready;
    unsigned int j;

    i = 0;
    j = 0;
    while (1) {
        ready = fifo_pcap_cache[i].buffer_ready;
        if ( ready == -1) {
            return 0;
        }
        if (ready==1) {
            //printf("Processing buffer %d\n", i);
            echo(i);   //! releasing within echo()
#ifdef PKT_ENDLESS
            i = (i+1) % total_files_num;
#else
            i = (i+1) % MaxBuffers;
#endif
        } else {
            j++;
            if (j == PRINT_LIMIT) {
                printf("Waiting for buffer %d free\n", i);
                j = 0;
            }
        }
    }
}

void init_pcap_cache(int N)
{
    int i;
    for (i=0; i<N; i++) {
        fifo_pcap_cache[i].buffer_ready = 0;
    }
}

char *meta_filename;

int main(int argc, char **argv)
{
    int ifindex = -1;
    int i;
    int core1 = 0;	/*main thread*/

    char *addr = "127.0.0.1";
    uint16_t port = 2055;

    iter_num = 1;   /* 1 time is enough */

	signal(SIGINT, show);

    for( i = 1; i< argc; i++) {
        if(strcmp(argv[i], "-f") == 0) {
            meta_filename = argv[i+1];
            continue;
        }
        if(strcmp(argv[i],"-s") == 0) {
            speed_loop = atoi(argv[i+1]);
            continue;
        }
        if(strcmp(argv[i],"-t") == 0) {
            iter_num = atoi(argv[i+1]);
            continue;
        }
        if (strcmp(argv[i], "-l") == 0) {
            speed_loop = atoi(argv[i + 1]);
            continue;
        }
        if(strcmp(argv[i], "-a") == 0) {
            addr = argv[i+1];
            continue;
        }
        if(strcmp(argv[i], "-p") == 0) {
            port = atoi(argv[i+1]);
            continue;
        }
    }

    //assert(devname !=NULL);

#ifdef PKT_ENDLESS

int get_files_num(FILE * fp);

    FILE * fp;
    if((fp = fopen(meta_filename, "rb")) != NULL) {
        total_files_num = get_files_num(fp);
        if(total_files_num == 0) {
            printf("An empty trace list file.\n");
            return 0;
        }

        printf("###Total pcap files num: %d\n", total_files_num);
    }
#endif
    mybind_cpu(core1);
    init_pcap_cache(MaxBuffers);

    printf("init udp addr: %s, port: %d\n", addr, port);
    initUdp(addr, port);

    //pthread_create(&open_file_ctrl, NULL, (void *)open_files, (void *)(long)core2);
    //printf("%d\n",ifindex);
    open_files((void *)(long)core1);

    while (1) {
        sending_packets(ifindex);
    }

    pthread_join(open_file_ctrl, NULL);

    printf("%d over sized packets dropped\n", over_sized_packets);

    return 0;
}
