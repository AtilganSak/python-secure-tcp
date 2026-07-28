import ipaddress
import socket
import ssl
import sys

def is_ip(s):
    try:
        ipaddress.ip_address(s)
        return True
    except ValueError:
        return False

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_socket = context.wrap_socket(client_socket, server_hostname='localhost')

ip_try_counter = 0
while True:
    ip = input("IP: ")
    if not is_ip(ip):
        ip_try_counter += 1
        if ip_try_counter == 3:
            print("Quitting...")
            sys.exit()
        else:
            print("Invalid IP! Please try again!")
    else:
        break

port_try_counter = 0
while True:
    port = int(input("Port: "))
    if 0 <= port <= 65535:
        break
    else:
        port_try_counter += 1
        if port_try_counter == 3:
            print("Quitting...")
            sys.exit()
        else:
            print("Invalid Port! Please try again!")
try:
    secure_socket.connect((ip,port))
    print("Connected server")
    print("Type 'quit' to exit")
    while True:
        message = input("Message: ")
        if message == "quit":
            break

        secure_socket.send(message.encode('utf-8'))
        print(f"Client: {message} ✔✔")
        data = secure_socket.recv(1024)
        print(f"Server: {data.decode('utf-8')}")
        
except ConnectionRefusedError:
    print("Server unavailable!")

secure_socket.close()
