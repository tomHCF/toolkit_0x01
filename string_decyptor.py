#!/usr/bin/python2
#pip install lief==0.9.0

import yara
import struct
import sys
import lief
from Crypto.Cipher import ARC4

#python2 string_deryptor.py <decrypted dex>

def RC4_dec(key, msg):
    try:
        return ARC4.new(key).decrypt(msg)
    except:
        return "\x00"

def dec_str_1(dex_file):
    dex = lief.DEX.parse(dex_file)
    for strc in dex.strings:
        if len(strc) >= 16 and strc[-1] != ";": #and len(strc) %4 ==0
            try:
                print "{} --> {}".format(strc, RC4_dec(strc[:12], strc[12:].decode('base64').decode('hex')))       
            except:
                pass
 
def dec_str_2(dex_file, key):
    dex = lief.DEX.parse(dex_file)
    for strc in dex.strings:
        if len(strc) >= 4 and strc[-1] != ";" and len(strc) %4 == 0: 
            try:
                print "{} --> {}".format(strc, RC4_dec(key, strc.decode('base64').decode('hex')))
            except:
                pass

rule_source_byte = '''
rule bytecode {
	strings:
		$bytecode01 = { 70 10 ?? ?? 04 00 12 10 5C 40 ?? ?? 5C 40 ?? ?? 5C 40 ?? ?? 1A 01 ?? ?? 5B 41 ?? ?? 1A 01 ?? ?? 5B 41 ?? ?? 1A 01 ?? ?? 70 20 ?? ?? 14 00 0C 01 5B 41 ?? ?? 1A 01 ?? ?? 70 20 ?? ?? 14 00 0C 01 5B 41 ?? ?? 1A 01 ?? ?? 70 20 ?? ?? 14 00 0C 01 5B 41 ?? ?? 1A 01 ?? ?? 70 20 ?? ?? 14 00 0C 01 5B 41 ?? ?? 1A 01 ?? ?? 70 20 ?? ?? 14 00 0C 01 5B 41 ?? ?? 1A 01 ?? ?? 70 20 ?? ?? 14 00 0C 01 5B 41 ?? ?? 1A 01 ?? ?? 70 20 ?? ?? 14 00 0C 01 5B 41 ?? ?? 1A 01 ?? ?? 70 20 ?? ?? 14 00 0C 01 5B 41 ?? ?? 1A 01 ?? ?? 70 20 ?? ?? 14 00 0C 01 5B 41 ?? ?? 12 51 23 11 }
		$bytecode02 = { 70 10 ?? ?? 04 00 12 10 5C 40 ?? ?? 12 01 5C 41 ?? ?? 5C 4? ?? ?? 1A 02 ?? ?? 5B 42 ?? ?? 1A 02 ?? ?? 5B 42 ?? ?? 1A 02 ?? ?? 70 20 ?? ?? 24 00 0C 02 5B 42 ?? ?? 1A 02 ?? ?? 70 20 ?? ?? 24 00 0C 02 5B 42 ?? ?? 1A 02 ?? ?? 70 20 ?? ?? 24 00 0C 02 5B 42 ?? ?? 1A 02 ?? ?? 70 20 ?? ?? 24 00 0C 02 5B 42 ?? ?? 1A 02 ?? ?? 70 20 ?? ?? 24 00 0C 02 5B 42 ?? ?? 1A 02 ?? ?? 70 20 ?? ?? 24 00 0C 02 5B 42 ?? ?? 1A 02 ?? ?? 70 20 ?? ?? 24 00 0C 02 5B 42 ?? ?? 1A 02 ?? ?? 70 20 ?? ?? 24 00 0C 02 5B 42 ?? ?? 1A 02 ?? ?? 70 20 ?? ?? 24 00 0C 02 5B 42 ?? ?? 12 52 23 22 }
	condition:
		1 of them
}
'''
rule_source_ind_dex = '''
rule ind_dex_1 {
	strings:
		$text_String01 = "||youNeedMoreResources||"
		$text_String02 = "LOADING INJECT++++++++"
		$text_String03 = "F2Tb"
		$text_String04 = "HideInject"
	condition:
		all of them
}

rule ind_dex_2 {
	strings:
		$text_String01 = "KKOKLKKKKLKKKKKKKKKKLKKKKKKK"
		$text_String02 = "xiaomi"
		$text_String03 = "No permissions to get contacts"
		$text_String04 = "Etkinle"
	condition:
		all of them
}
'''
def yara_scan_byte(raw_data):
	offset = 0
	yara_rules = yara.compile(source=rule_source_byte)
	match = yara_rules.match(data=raw_data)
	for item in match[0].strings:
		offset = (item[1], item[0])
	return offset
	
def yara_scan_ind_dex(raw_data):
	dex_type = 0
	yara_rules = yara.compile(source=rule_source_ind_dex)
	matches = yara_rules.match(data=raw_data)
	for match in matches:
		if match.rule == 'ind_dex_1':
			dex_type = 1
			return dex_type
		elif match.rule == 'ind_dex_2':
			dex_type = 2
	return dex_type

def readof(dfile, offset, nbytes):
	dfile.seek(offset)
	return dfile.read(nbytes)

def get_RC4_pass(dex_data, off):
	if off[0] == '$bytecode01':
		offw = 0x1E
	if off[0] == '$bytecode02':
		offw = 0x20
	offset = off[1] + offw
	string_id = struct.unpack("<H", readof(dex_file, offset, 2))[0]
	string_ids = struct.unpack("<I", readof(dex_file, 0x3c, 4))[0]
	dex_file.seek(string_ids + string_id * 4)
	str_addr = struct.unpack("<I", readof(dex_file, string_ids + string_id * 4, 4))[0] + 1
	return readof(dex_file, str_addr, 0xc)

dex = sys.argv[1]
dex_file = file(dex, 'rb')
dex_data = dex_file.read()
con = yara_scan_ind_dex(dex_data)
if con == 1:
	dec_str_1(dex)
elif con == 2:
	offset = yara_scan_byte(dex_data)
	key = get_RC4_pass(dex_data, offset)
	dec_str_2(sys.argv[1], key)
	print "RC4 string decryption key : {}".format(key)
else:
	print "not found"
dex_file.close()


