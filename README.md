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
```
 the code above is our main 
