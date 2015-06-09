#ifndef _PKT_BUFF_H
#define _PKT_BUFF_H
#include <stdio.h>
#include <sys/types.h>


#if !defined(__USE_GNU)
#define  __USE_GNU 1
#endif

#include <sched.h>
#include <pthread.h>

/*pcap file format*/
typedef struct pf_hdr {
	u_int32_t	 magic;
	u_int16_t	 version_major;
	u_int16_t	 tversion_minor;
	int32_t	 thiszone;  /* gmt to local correction */
	u_int32_t	 sigfigs; /* accuracy of timestamps */
	u_int32_t	 snaplen; /* max length saved portion of each pkt */
	u_int32_t	 linktype;   /* data link type (LINKTYPE_*) */
} pf_hdr_t;

typedef struct pcaprec_hdr_s {
	 u_int32_t	 ts_sec;         /* timestamp seconds */
	 u_int32_t	 ts_usec;        /* timestamp microseconds */
	 u_int32_t	 ncl_len;       /* number of octets of packet saved in file */
	 u_int32_t	 rig_len;       /* actual length of packet */
} p_hdr_t;

struct file_cache {
	char *fcache;
	unsigned long offset;
	unsigned long size;
#if defined(CACHE_LL)
	struct file_cache *next;
#endif
	FILE   *fp;
	/*pcap header*/
	pf_hdr_t hdr;
};

typedef struct file_cache 	file_cache_t;

#define PADDING   (64)
#define PAD(suffix, type, type1) char padding ## suffix [PADDING - sizeof(type)-sizeof(type1)]

typedef struct _fifo_pcap_elem {
   file_cache_t       pcap_cache_trace;
   volatile int       buffer_ready;
} FIFO_PCAP_ELEM;

#define MaxFileNameLen   (512)

#ifdef PKT_ENDLESS
#define MaxBuffers       (512)
#else
#define MaxBuffers       (66)
#endif

extern char          traceName[MaxBuffers][MaxFileNameLen];
extern FIFO_PCAP_ELEM fifo_pcap_cache[MaxBuffers];
extern char   * meta_filename;

extern u_char *prep_next_skb(file_cache_t *fct,u_int32_t *pktlen, int); 
extern int 	check_pcap(file_cache_t *fct); 
extern void 	hex_printk(unsigned char *str,int len);
extern void 	release_pkt_buff_part(void);
extern int 	release_pkt_buff(int i);
extern file_cache_t    *preload_pcap_file(char * filename, int i);
extern void     open_files(void *);

#endif 
