#include <stdio.h>
#include <string.h>

void removenotchar(char* c)
{
    char *last=c;
    while(*c)
    {
        if (*c<0) {
            c++;
        } else {
            *last=*c;
            last++;
            c++;
        }
    }
    *last=0;
}


int main()
{
    char m[]="{'refer':'company=昆山市园洲仪表有限公司','user_agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 708; 360SE)'}";
    removenotchar(m);
    printf("%s",m);
    return 0;
}
