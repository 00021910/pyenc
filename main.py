# string encrypt/decrypt
# relies on the keymap.data file, should be in the same directory

# let's import some modules to work with files
import os, sys 

# also random too because we are building an encryptor lol
from random import randint

d_keymap = {}

p_keymapFilePath = "./keymap.kmp"

f_keymapFile = open(p_keymapFilePath, "r")

for s_line in f_keymapFile:
    arr_tmp = s_line.split()
    s_key = arr_tmp[0]
    s_val = arr_tmp[1]
    if s_key == "EMPTY": s_key = " "
    d_keymap[s_key] = int(s_val)

def list_unstring(stringified_list):
    return stringified_list.strip("][").split(", ")

def str_to_binary(string_sample):
    return ' '.join(format(ord(x), 'b') for x in string_sample)

def bin_to_string(binary_sample):
    binary_vals = binary_sample.split()
    string_res = ""
    for i in binary_vals:
        an_int = int(i, 2)
        ascii_char = chr(an_int)
        string_res += ascii_char
    return string_res

def encrypt(cleartxt, key, use_binary=False):
    ivseed = randint(350, 4294967296)
    print(f"generated IV seed: {ivseed}")
    encodedbuff = []
    for i in str(cleartxt):
        encodedbuff.append(d_keymap[i])
    print(f"encoded string: {str(encodedbuff)}")

    cipherstream = []
    cipherstream.append(ivseed)
    compkey = ivseed + int(key)
    for i in encodedbuff:
        encryptedbyte = (3 * i) + int(compkey)
        cipherstream.append(encryptedbyte)
    print(f"encrypted string: {str(cipherstream)}")
    encfile = open("enrypted.txt", 'w')
    realstdout = sys.stdout
    outstr = str(cipherstream)
    if use_binary: outstr = str_to_binary(outstr)
    sys.stdout = encfile
    print(outstr)
    sys.stdout = realstdout
    encfile.close()
    return cipherstream

def decrypt(cipherstream, key, use_binary=False):
    if use_binary: 
        ciphertext = list_unstring(bin_to_string(cipherstream))
    else:
        if type(cipherstream) == 'string':
            ciphertext = list_unstring(cipherstream)
        else: 
            ciphertext = cipherstream
    encodedbuff = []
    for i in ciphertext:
        encodedbuff.append(int(i))
    decrypted_signal = []
    readiv = encodedbuff[0]
    print(f"read IV seed: {readiv}")
    compkey = int(readiv) + int(key)
    print(f"composite key: {compkey}")
    for i in encodedbuff:
        decrypted_signal.append(int((i - int(compkey)) / 3))
        print(f"decrypted signal: {decrypted_signal}")
    decrypted_text = []
    for i in decrypted_signal:
        for k, v in d_keymap.items():
            if v == i:
                decrypted_text.append(k)
    print(f"decrypted string as a list: {decrypted_text}")
    decrypted_text_str = ''
    for i in decrypted_text:
        decrypted_text_str += str(i)
    print(f"decrypted string: {decrypted_text_str}")
    return decrypted_text_str

string = "Hello world! :3"
key = 133742069
encrypted = encrypt(string, key)
decrypted = decrypt(encrypted, key)
print(string, encrypted, decrypted)