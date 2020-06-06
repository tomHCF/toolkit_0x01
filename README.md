## **Toolkit for analysis Android malware**

 
This repository contains tools to reverse enginiring Android malware Cerberus. For analysing Android malware I highly rocomend this sandbox https://apkdetect.com/ by https://twitter.com/pr3wtd


Cerberus malware uses several anti-revering techniques. One of them is packer - it loads class at runtime from file. The Dex file is stored in application resources  (asset directory). The File is encrypted using RC4 algorythm and pretends to be a json file. Next anti-reversing technique is string encryption. For example, the CnC address is stored in this form. During research, I noticed two types of this dex file, probably different versions. It is possible there are more versions. 
One of the differences between them is the method of string encryption

Repository contains tool for extracting decrypted dex file and string decryption:
1. enc_dex_brutforce.py - script for brutforcing RC4 key and decrypt dex file. This script is not the best solution for retriving dex file, but it's woth to try, sometime key is short. Usage:
 `python enc_dex_brutforce.py <encrypted dex>`
2. dex_dump.py and dex_dump.js - scripts for dynamicy retriving dex file based on Frida (https://frida.re/). It also logs several syscalls as write, open, read, unlink. Other malware, e.g. Gnip, Hydra uses a similar packer, so you can use these scripts to extract the dex file. Usage:
	`python dex_dump.py dex_dump.js <package name of malicious apk> <working directory>`

3. string_decryptor.py - decrypts strings in a dex file. The script detects
type of strings encryption and then selects proper method to decrypt. Usage:
 `python string_deryptor.py <decrypted dex file>`
