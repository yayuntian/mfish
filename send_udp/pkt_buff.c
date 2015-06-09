#define _FILE_OFFSET_BITS 64
#include "pkt_buff.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define FILE_BASE_SIZE  (1024*1024*1024ULL) /*BYTE*/

#if defined(LARGE_FILE)
#define FILE_CACHE_SIZE (10*FILE_BASE_SIZE) /*BYTE*/
#else
#define FILE_CACHE_SIZE (FILE_BASE_SIZE) /*BYTE*/
#endif

extern int over_sized_packets;


#if defined(CACHE_LL)
file_cache_t 	*file_cache_head=NULL;
#endif

#define FOFFSET(n) fct->offset += (n)
#define TCPDUMP_MAGIC      0xa1b2c3d4 /*no swap, and tcpdump pcap format*/

#define MaxPacketLen  (1512+10)
/*
 *build next skb from buffer cache
 */
u_char *prep_next_skb(file_cache_t *fct,u_int32_t *pktlen, int i)
{
    /* if end */
//next_packet:
    if (fct->offset == fct->size) {
        printf("LOAD FILE COMPLETE: %s\n", traceName[i]);
        return NULL;
    }
    if (fct->offset > fct->size) {
        printf("Wrong data %ld > %ld in %s\n", fct->offset, fct->size, traceName[i]);
        return NULL;
    }
    if(fct->offset + sizeof(p_hdr_t) >= fct->size) {
        printf("Garbage data found at the end of file.\n");
        return NULL;
    }

    /*set packet data and hdr pointer,? no copy*/
    p_hdr_t *hdr = (p_hdr_t*)(fct->fcache + fct->offset);
    u_int32_t caplen = hdr->ncl_len;
    //! move the header
    FOFFSET(sizeof(p_hdr_t));
    u_char *pktdata = (u_char *)(fct->fcache + fct->offset);

    //! move the packet
    FOFFSET(hdr->ncl_len);

    if (caplen >= MaxPacketLen) {
        printf("Wrong length %u at offset %lu in %s.\n", caplen, fct->offset, traceName[i]);
        //over_sized_packets++;
        //goto next_packet;
    }

    if (fct->offset > fct->size) {
        if (fct->offset < (fct->size + MaxPacketLen)) {
            printf("Last packet is thrown away in %s.\n", traceName[i]);
        } else {
            printf("File size %ld in %s is wrong!\n", fct->offset, traceName[i]);
        }
        return NULL;
    }

    *pktlen = caplen;

    return pktdata;
}

int check_pcap(file_cache_t *fct)
{
    u_int32_t magic;
    int size;
    char *ch;
    memcpy((char *) &magic, fct->fcache + fct->offset, sizeof(magic));
    FOFFSET(sizeof(magic));
    if (magic != TCPDUMP_MAGIC) {
        printf("<1> NOT a tcpdump file.\n");
        return 0;
    }
    fct->hdr.magic = magic;

    size = sizeof(fct->hdr)-sizeof(magic);
//!     Wrong use of pointer arithematic
//!     memcpy(&(fct->hdr)+sizeof(magic), fct->fcache+fct->offset, size);
//!
    ch = (char *) &(fct->hdr)+sizeof(magic);
    memcpy(ch, fct->fcache+fct->offset, size);
    FOFFSET(size);

    if (fct->offset >= fct->size) {
        printf("<1> NOT a complete pcap file.\n");
        return 0;
    }
    return 1;
}


file_cache_t *preload_pcap_file(char * filename, int b_i)
{

    FILE	*fp;
    char 		*fcache=NULL;
    unsigned long 	size, size1;
    file_cache_t 	*fct;
    char errbuf[256];

    fp = fopen(filename, "rb");

    if (!fp) {
        printf("Cannot open file: %s.\n", filename);
        printf("File: %s will NOT be processed.\n", filename);
        return NULL;
    }

    fseek(fp, 0, SEEK_END);
    size = ftell(fp);
    fseek(fp, 0, SEEK_SET);

    if (size > FILE_CACHE_SIZE) {
        printf("File size %lu is too big, and please increase CACHE_SIZE.\n", size);
        return NULL;
    }
    fcache = malloc(size);
    if (fcache == NULL) {
        printf("<1> vmalloc file cache failed!\n");
        fclose(fp);
        return NULL;
    }

    size1 = fread((void *)fcache, (size_t)1, (size_t) size, fp);

    if (size1 == 0) {
        free(fcache);
        printf("kernel file read failed.\n");
        fclose(fp);
        return NULL;
    } else if (size1 < size) {
        free(fcache);
        fclose(fp);
        printf("<1>File cache size is not enough to buffer file.\n");
        return NULL;
    } else {
        printf("++++++ [%d]Loaded %ld Bytes from %s.\n", b_i, size, filename);
    }

    fclose(fp);

    /*save malloc pointer for vfree*/
    fct = &fifo_pcap_cache[b_i].pcap_cache_trace;
    memset(fct, 0, sizeof(file_cache_t));

#if defined(CACHE_LL)
    if (file_cache_head == NULL) {
        fct->next = NULL;
        fct->size = size;
        fct->fcache = fcache;
        file_cache_head = fct;
    } else {
        fct->next = file_cache_head;
        fct->fcache = fcache;
        fct->size = size;
        file_cache_head = fct;
    }
#else
    fct->fcache = fcache;
    fct->size   = size;
#endif

    /* avoid warning in compliation*/
    if (errbuf[0] != 0);
    return fct;
}


void release_pkt_buff_part()
{
#if defined(CACHE_LL)
    /*free vmalloc buffer cache*/
    file_cache_t *fct=file_cache_head;
    file_cache_t *next=file_cache_head->next;
    while(fct!=NULL) {
        free(fct->fcache);
        free(fct);
        fct=next;
        if(next!=NULL)
            next=next->next;
    }

    printf("<1>Buffer cache free done!\n");
#endif
    return ;
}

int release_pkt_buff(int i)
{
    /*free vmalloc buffer cache*/
    file_cache_t *fct= &fifo_pcap_cache[i].pcap_cache_trace;
#ifdef PKT_ENDLESS
    if (fct) {
        fifo_pcap_cache[i].buffer_ready = 0;

        char *fcache = fct->fcache;
        unsigned long size = fct->size;

        memset(fct, 0, sizeof(file_cache_t));

        fct->fcache = fcache;
        fct->size   = size;

        if(!check_pcap(fct)) {
            printf("%s is not a correct trace file.\n", traceName[i]);
            return 0;
        }
        fifo_pcap_cache[i].buffer_ready = 1;
        printf("------ Buffer cache %d for %s is refresh.\n", i, traceName[i]);

    }
#else
    if (fct) {
        free(fct->fcache);   //! Buffer is freed
        fifo_pcap_cache[i].buffer_ready = 0;
        printf("------ Buffer cache %d for %s is free.\n", i, traceName[i]);

    }
#endif
    return 1;
}

void hex_printf(unsigned char *str,int len)
{

    int times=len/16;
    int last=len%16;
    unsigned char *p=str;
    int i=0;
    for(i=0; i<times; i++) {
        printf("<1>data:%2x %2x %2x %2x %2x %2x %2x %2x %2x %2x %2x %2x %2x %2x %2x %2x\n", \
               p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10],p[11],p[12],p[13],p[14],p[15]);
        p+=16;
    }
    printf("<1>Remained %d data have been shown\n",last);

}
