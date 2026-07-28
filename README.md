# Python Secure TCP Communication (TLS Sockets)

This project is a foundational client-server application designed to demonstrate secure network programming in Python. It uses the standard `socket` library for TCP communication, and all data traffic is encrypted via the modern **TLS protocol** using Python's built-in `ssl` module.

It is an excellent starting point for understanding how network packets are encrypted (which can be observed via tools like Wireshark) and how data is protected against Man-in-the-Middle (MitM) attacks.

## Features
* Communication over standard TCP sockets.
* End-to-end encryption with TLS (Transport Layer Security).
* Uses self-signed certificates for local testing and development.

## Prerequisites
To run this project, you need to have the following installed on your system:
* Python 3.x
* OpenSSL (to generate the required certificates)

---

## Installation and Usage

You cannot run the project immediately after cloning it. To enable encryption, you first need to generate your local test certificates.

### 1. Generating SSL Certificates (OpenSSL)

We need a public certificate (`cert.pem`) and a private key (`key.pem`) to encrypt the traffic between the client and the server.

Open your terminal or command prompt in the project directory and run the following OpenSSL command:

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
