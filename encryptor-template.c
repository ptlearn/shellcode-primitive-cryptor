#include <stdio.h>
#include <stdlib.h>
#include <string.h>

CLEAR_SHELLCODE_POINT


unsigned char *xor_key = "KEY_POINT";

int symbols_limit_by_line = 24;

static unsigned char *xor_func_with_print(unsigned char *buf, size_t mlen) {
    size_t keylen = strlen(xor_key);

    unsigned char *enc = (unsigned char *) malloc(mlen + 1);
    memset(enc, 0, mlen + 1);

    int i;

    printf("unsigned char shellcode[] =\n");

    for(i = 0; i < mlen; i++) {
        if (i % symbols_limit_by_line == 0) {
            if (i == 0) {
                printf("\"");
            } else {
                printf("\"\n\"");
            }
        }

        enc[i] = buf[i] ^ xor_key[i % keylen];
        printf("\\x%02X", (unsigned) enc[i]);
    }

    if (i % symbols_limit_by_line == 0) {
        printf(";\n");
    } else {
        printf("\";\n");
    }

    printf("\n");
    // enc[mlen] = '\0';

    return enc;
}



int main(void) {
    xor_func_with_print(shellcode, sizeof(shellcode));
    return 0;
}
