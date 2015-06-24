#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT   (64*1024*1024)
#define MASK    (COUNT - 1)

void main(int argc, char **argv)
{
    int *arr;
    int i;
    int *p;
    int step = 1;

    if (argc == 2){
        step = atoi(argv[1]);
    }

    arr = (int *)malloc(sizeof(int) * COUNT);

    if (!arr) {
        printf("malloc error!\n");
        exit(0);
    }
    memset(arr, 0x00, sizeof(int) * COUNT);

    for (i = 0; i < COUNT; i++){
        arr[((i * step) & MASK)]++;
    }
}
