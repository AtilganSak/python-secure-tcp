import socket
import subprocess
import sys
import ipaddress
import ssl

rule_name = "Python_TCP_Server_Rule"


def set_firewall_rule(port_number):
    command = [
        "netsh", "advfirewall", "firewall", "add", "rule",
        f"name={rule_name}",
        "dir=in",
        "action=allow",
        "protocol=TCP",
        f"localport={port_number}"
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print("Added firewall rule successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error cause: {e.stderr}")
        return False


def remove_firewall_rule():
    command = [
        "netsh", "advfirewall", "firewall", "delete", "rule",
        f"name={rule_name}"
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print("Removed firewall rule successfully!")

    except subprocess.CalledProcessError as e:
        print(f"Error cause: {e.stderr}")


def is_ip(s):
    try:
        ipaddress.ip_address(s)
        return True
    except ValueError:
        return False


def main():
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

    is_completed_firewall = set_firewall_rule(port)

    if not is_completed_firewall:
        print("Doesn't set firewall rule! Quitting...")
        sys.exit()

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    print("Server started and listening now!")
    server.listen()

    conn, addr = server.accept()
    secure_socket = context.wrap_socket(conn, server_side=True)
    with conn:
        print(f"Connected: {addr[0]}:{addr[1]}")
        print("Type 'quit' to exit")
        print("Waiting first message...")
        while True:
            data = secure_socket.recv(1024)
            if not data:
                print("Client disconnected!")
                break
            print(f"Client: {data.decode('utf-8')}")

            answer = input("Message: ")
            secure_socket.send(answer.encode('utf-8'))
            print(f"Server: {answer} ✔✔")

    print("Server shutting down...")
    remove_firewall_rule()
    server.close()


if __name__ == "__main__":
    main()
