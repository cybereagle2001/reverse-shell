# Reverse-Shell
A reverse shell is a shell session established on a connection that is initiated from a remote machine, not from the attacker’s host. Attackers who successfully exploit a remote command execution vulnerability can use a reverse shell to obtain an interactive shell session on the target machine and continue their attack. Reverse shells can also work across a NAT or firewall.
One of the most known frameworks that ethical hackers use in order to create and commnunicate with a reverse shell is MSFVenom and MSFconsole. 

How does it work?? 
To understand the mecanism i decided to write a simple reversehell in python in order to expalin the basics of the reverse shell theory.

# Requirements
To do so we need these common python libraries: 

### socket:
This module provides access to the BSD socket interface. It is available on all modern Unix systems, Windows, MacOS, and probably additional platforms.
The Python interface is a straightforward transliteration of the Unix system call and library interface for sockets to Python’s object-oriented style: the socket() function returns a socket object whose methods implement the various socket system calls. Parameter types are somewhat higher-level than in the C interface: as with read() and write() operations on Python files, buffer allocation on receive operations is automatic, and buffer length is implicit on send operations.

### OS
This module provides a portable way of using operating system dependent functionality. We are going to use this library in order to execute the commands sent by the attacker on the victim machine

### sys
Python sys module has several methods and variables that can alter various aspects of the Python runtime environment. It permits operating on the interpreter by giving access and information about the constants, variables, and functions that have a strong interaction with the interpreter.

### subprocess
The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.

# Code explication

## server.py
this is the script the hacker will be running on his machine/server this code is going to accpet and establish communication with the client side.

Coding the server side we only need the sockett libaray.

```
server_host= "0.0.0.0"
server_port= 443
data_size = 1024 * 128
SEPARATOR = "<sep>"
cyber = socket.socket()
```
As you can understanf from the variable names the server_host is the IP address of our server/attacker_machine we used the IP 0.0.0.0 in order to make the server reachable through all the IPv4 addresses of the server. For the server_port I used the port 443. We can use any port we want but the port 80 and 443 are widely used to bypass firewalls. data_size is the maximum ammoun of data that the client can send to the server and versversa.
SPERATOR is the seperation between the data sent or received.

then I created a socket and I called it cyber this is what we are going to use in the second part of our code.

Let's bind the socket that we created to out server IP and port that we initiated in the first two commands.
```
cyber.bind((server_host,server_port))
```
One of the most important part in creating such server is that it should have the ability to listen and accept incoming requests that why we need this two lines:
```
cyber.listen(10)
client_socket, client_ip = cyber.accept()
```
the listen function will allow us to listen to the incoming connections and the paramater 10 I used is the maximum length to which the queue of pending connections for sockfd may grow. That means if we receive 12 requests before we accept the connection then 2 of these requests will be droped.
The second line means that we accepted the connection from the client (our victim machine) and we stored the victim_socket and the victim_adress in two different variabales.
```
print(f"{client_ip[0]}:{client_ip[1]} Connected!")
```
This output will have the following format IP:PORT connected!
The first step we will do after having a connected client is to try and get the working directory on the victims devices this is why we will use the following code:
```
cmd = client_socket.recv(data_size).decode()
print("[+] Current working directory:", cmd)
```
