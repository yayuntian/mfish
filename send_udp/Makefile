.PHONY: clean

CFLAGS = -DPKT_ENDLESS

all: tx_pcap server

tx_pcap: echo.c pkt_buff.c open_files.c udp.c
	gcc  -O0 -g -Wall $(CFLAGS) -o tx_pcap echo.c pkt_buff.c open_files.c udp.c

server: server.c
	gcc  -g -Wall -o server server.c

clean:
	rm -f tx_pcap server
