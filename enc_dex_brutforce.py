#!/usr/bin/python2

import sys
from Crypto.Cipher import ARC4
from itertools import product
import string

# python2 enc_dex_brutforce.py <encrypted dex>

def RC4_dec(key, msg):
    try:
        return ARC4.new(key).decrypt(msg)
    except:
        return "\x00"

def brf_dex(dex_crypt, ind):
    charset = string.ascii_uppercase + string.ascii_lowercase + string.digits
    for i in range(ind+1):
        for attempt in product(charset, repeat=i):
            dex_magic = RC4_dec(''.join(attempt) ,dex_crypt) 
            if dex_magic[:5] ==  "\x64\x65\x78\x0a\x30":
                return ''.join(attempt)
    return 0

crypt_dex = sys.argv[1]
file_out = "out_" + crypt_dex  +".dex"
dex_crypt_ = open(crypt_dex, "rb")
dex_crypt = dex_crypt_.read()
dex_crypt_.close()
passwd =  brf_dex(dex_crypt[:5], 5)
if passwd == 0:
    print "key not found"
    exit()
print "key: {}".format(passwd)

