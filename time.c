#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <sys/time.h>
#include <errno.h>

void PrintMsg(int Num)
{

    struct timeval timep;

    gettimeofday(&timep, NULL);

    printf("sec: %d, usec: %d\n", timep.tv_sec, timep.tv_usec);
    printf("%s\n", "Hello World");

    return;
}

int main(int argc, char* argv[])
{
    signal(SIGALRM, PrintMsg);

    struct itimerval tick;
    tick.it_value.tv_sec = 1;
    tick.it_value.tv_usec = 0;
    tick.it_interval.tv_sec  =0;
    tick.it_interval.tv_usec = 100 * 1000;

    int ret = setitimer(ITIMER_REAL, &tick, NULL);

    if ( ret != 0)
    {
        printf("Set timer error. %s \n", strerror(errno) );

        return -1;
    }

    printf("Wait!\n");

    getchar();

    return 0;
}
