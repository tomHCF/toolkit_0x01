#!/usr/bin/python3

import frida
import sys
import logging
import datetime
import json
import os

# python3 dex_dump.py <script name> <package name> <working directory>

scriptname = sys.argv[1]
fd = open(scriptname, "r")
apk_package = sys.argv[2]

if len(sys.argv) < 4:
    cwd_path = os.path.abspath(os.getcwd())
else:
    cwd_path = sys.argv[3]

logFileName = "{}\LOG_{}_{}.txt".format(cwd_path, apk_package, str(datetime.datetime.now().date()))  
logging.basicConfig(filename=logFileName, filemode='w', level=logging.INFO, format='%(asctime)s -- %(message)s', datefmt='%H:%M:%S')
print("Logging: {}".format(logFileName))

def on_message(message, data):

    if message['type'] == 'error':
        logging.error(message)		
    elif message['type'] == 'send':
        recv_data = message['payload']
        if recv_data['name'] == 'log':
            logging.info(recv_data['log_'])
        if recv_data['name'] == 'file':
            filename = "{}\dump_DEX_{}.dex".format(cwd_path, str(datetime.datetime.now().strftime("%H_%M_%S")))
            file = open(filename, "wb")
            file.write(data)
            file.close()
            print("DEX dumped: {}".format(filename))
    else:
        print(message)
    
device = frida.get_usb_device()
pid = device.spawn([apk_package])
session = device.attach(pid)
script = session.create_script(fd.read())
fd.close()
script.on('message', on_message)
script.load()
device.resume(pid)
sys.stdin.read()
