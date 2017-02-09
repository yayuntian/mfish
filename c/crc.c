#include <stdio.h>
#include <stdint.h>
#include <nmmintrin.h>


static inline uint32_t hash_tuple4_sse_asym(const uint32_t sip, const uint32_t dip,
    const uint16_t sport, const uint16_t dport)
{
    uint32_t port = (uint32_t)sport << 16 | dport;
    uint64_t ip = (uint64_t) sip << 32 | dip;

    uint64_t crc1 = 0;
    crc1 = _mm_crc32_u64(crc1, ip);
    printf ("crc1 value : %lX\n", crc1);
    crc1 = _mm_crc32_u32(crc1, port);

    return crc1;
}

static inline uint32_t hash_u32(uint32_t a)
{
    a = (a + 0x7ed55d16) + (a << 12);
    a = (a ^ 0xc761c23c) ^ (a >> 19);
    a = (a + 0x165667b1) + (a << 5);
    a = (a + 0xd3a2646c) ^ (a << 9);
    a = (a + 0xfd7046c5) + (a << 3);
    a = (a ^ 0xb55a4f09) ^ (a >> 16);
    return a;
}

static inline uint64_t hash64shift(uint64_t key)
{
    key = (~key) + (key << 21); // key = (key << 21) - key - 1;
    key = key ^ (key >> 24);
    key = (key + (key << 3)) + (key << 8); // key * 265
    key = key ^ (key >> 14);
    key = (key + (key << 2)) + (key << 4); // key * 21
    key = key ^ (key >> 28);
    key = key + (key << 31);

    printf("64 hash: %lx\n", key);
    return key;
}


static inline uint64_t hash_tuple4_asym(const uint32_t sip, const uint32_t dip,
    const uint16_t sport, const uint16_t dport)
{
    uint32_t port = (uint32_t)sport << 16 | dport;
    uint64_t ip = (uint64_t) sip << 32 | dip;

    uint64_t res;

    res = hash_u32(port);
    res ^= hash64shift(ip);

    //return res & 0xffffffff;
    return res;
}


int main (int argc, char *argv [])
{
    uint32_t sip = 3549626657; 
    uint32_t dip = 758716684;

    uint16_t sport = 5566;
    uint16_t dport = 80;

    uint64_t res;

    uint64_t ip = (uint64_t) sip << 32 | dip;

    printf ("CRC32 result : %lX\n", ip);
    res = _mm_crc32_u64(0, ip);
    printf ("CRC32 result : %lX\n", res);


    return 0;
}
