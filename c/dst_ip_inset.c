#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/time.h>
#include <string.h>


#define TOP     100
static int mid[500] = {49, 34, 23, 15, 12, 7, 7, 6, 5, 3, 2, 1, 0};

static int dst_ip_inset(int *mid_aggs, int value)
{
    // mid_aggs table is desc by ip address
    if (value > mid_aggs[0] || value < mid_aggs[TOP - 1]) {
        return -1;
    }
    int left = 0, right = TOP - 1;
    uint32_t cur = 0;
    while(left <= right) {
        int mid = left + ((right - left) >> 2);
        cur = mid_aggs[mid];
        if (value > cur) {
            right = mid - 1;
        } else if (value < cur) {
            left = mid + 1;
        } else {
            return mid;
        }
    }
    return -1;
}



void main(int argc, char *argv[])
{
    int ret, i;
    int num = atoi(argv[1]);
    printf("search: %d\n", num);

    for (i = 0; i < TOP; i++) {
        if (mid[i]) {
            printf("%d ", mid[i]);
        }
    }
    printf("\n");

    ret = dst_ip_inset(mid, num);
    printf("ret: %d\n", ret);
}



