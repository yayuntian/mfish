#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif
#define __USE_GNU

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <assert.h>
#include <string.h>
#include <time.h>
#include "pkt_buff.h"

char     traceName[MaxBuffers][MaxFileNameLen];
FIFO_PCAP_ELEM fifo_pcap_cache[MaxBuffers];
extern   int   iter_num;

int msleep()
{
    usleep(1000);
#if 0
    struct timespec req;
    req.tv_sec=0;
    req.tv_nsec=2000000L;
    while(nanosleep(&req,&req)==-1)
        continue;
#endif
    return 1;
}

int get_files_num(FILE * fp)
{
    int files_num;
    char tmp_name[128];
    char * tmp;
    if(fp == NULL) {
        printf("fp == NULL in function get_files_num.\n");
        return 0;
    }

    fseek(fp, 0, SEEK_SET);

    files_num = 0;
    while(1) {
        tmp = fgets(tmp_name, 128, fp);
        if(tmp == NULL) {
            fseek(fp, 0, SEEK_SET);
            return files_num;
        }
        if (tmp_name[0]=='#' || tmp_name[0]=='\n' || tmp_name[0]=='\r') {
            continue;
        }
        files_num++;
    }
}

#ifndef PKT_ENDLESS

void open_files(void *cpu_id)
{
    int i, j, k, length, total_times, files_num;
    char * filename = (char *)meta_filename;
    char * trace_file = NULL;
    FILE * fp;
    cpu_set_t mask;
    file_cache_t * fct;

    int id = (int)(long)cpu_id;
    CPU_ZERO(&mask);
    CPU_SET(id, &mask);
    if(sched_setaffinity(0, sizeof(cpu_set_t), &mask) < 0) {
        printf("Error: sched_setaffinity failed in function open_files.\n");
        exit(0);
    }

    if((fp = fopen(filename, "rb")) != NULL) {
        /* get the number of trace files. */
        files_num = get_files_num(fp);

        /* file_num == 0, exit. */
        if(files_num == 0) {
            printf("An empty trace list file.\n");
            exit(0);
        }

        /* get the total_times for loading files. */
        total_times = files_num * iter_num;

        /* buffer_index. */
        i = 0;

        /* load trace files. */
        for(j = 0; j < total_times; ++j) {
            /* waiting for buffer_ready to be 0. */
            while(fifo_pcap_cache[i].buffer_ready) {
                msleep();
            }

            trace_file = fgets(traceName[i], MaxFileNameLen, fp);
            assert(trace_file != NULL);
            /* an invaild line. */
            if (traceName[i][0]=='#' || traceName[i][0]=='\n' || traceName[i][0]=='\r') {
                j--;
                continue;
            }

            length = strlen(traceName[i]);
            traceName[i][length-1] = '\0';

            fct = preload_pcap_file(traceName[i], i);
            if(fct != NULL) {
                if(!check_pcap(fct)) {
                    printf("%s is not a correct trace file.\n", traceName[i]);
                    continue;
                }
            } else {
                printf("Load file %s failed.\n", traceName[i]);
                continue;
            }

            /* loaded file in success. */
            i++;

            /* MaxBuffers files loaded. */
            if(i == MaxBuffers) {
                for(k = 0; k < MaxBuffers; ++k) {
                    fifo_pcap_cache[k].buffer_ready = 1;
                }
                i = 0;
            }

            /* completed one or another round. */
            if(j % files_num == files_num-1) {
                fseek(fp, 0, SEEK_SET);
            }
        }

        /* for the left files. */
        for(k = 0; k < i; ++k) {
            fifo_pcap_cache[k].buffer_ready = 1;
        }

        /* wait to set exit flag. */
        while(fifo_pcap_cache[i].buffer_ready);
        fifo_pcap_cache[i].buffer_ready = -1;	//setting one exit flag is enough!

        fclose(fp);
    } else {
        printf("Can NOT open file %s.\n", filename);
        exit(0);
    }

    //pthread_exit(NULL);
}

#else
void open_files(void *cpu_id)
{
    int i, length, files_num;
    char * filename = (char *)meta_filename;
    char * trace_file = NULL;
    FILE * fp;
    cpu_set_t mask;
    file_cache_t * fct;

    int id = (int)(long)cpu_id;
    CPU_ZERO(&mask);
    CPU_SET(id, &mask);
    if(sched_setaffinity(0, sizeof(cpu_set_t), &mask) < 0) {
        printf("Error: sched_setaffinity failed in function open_files.\n");
        exit(0);
    }

    if((fp = fopen(filename, "rb")) != NULL) {
        /* get the number of trace files. */
        files_num = get_files_num(fp);

        /* file_num == 0, exit. */
        if(files_num == 0) {
            printf("An empty trace list file.\n");
            exit(0);
        }
        /* load trace files. */
        for(i = 0; i < files_num; i++) {

            trace_file = fgets(traceName[i], MaxFileNameLen, fp);
            assert(trace_file != NULL);
            /* an invaild line. */
            if (traceName[i][0]=='#' || traceName[i][0]=='\n' || traceName[i][0]=='\r') {
                i--;
                continue;
            }

            length = strlen(traceName[i]);
            traceName[i][length-1] = '\0';

            fct = preload_pcap_file(traceName[i], i);
            if(fct != NULL) {
                if(!check_pcap(fct)) {
                    printf("%s is not a correct trace file.\n", traceName[i]);
                    exit(0);
                }
            } else {
                printf("Load file %s failed.\n", traceName[i]);
                exit(0);
            }
            fifo_pcap_cache[i].buffer_ready = 1;
        }

        fclose(fp);
    } else {
        printf("Can NOT open file %s.\n", filename);
        exit(0);
    }
}
#endif
