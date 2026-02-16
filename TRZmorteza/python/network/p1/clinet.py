import socket
import re

ip_pattern = re.compile(r'^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}$')
port_pattern = re.compile(r'^\d{1,5}$')  

while not ip_pattern.match(HOST := input("Enter IP address: ")):
    print("Try again.")

while not port_pattern.match(port_str := input("Enter port: ")):
    print("Try again.")

PORT = int(port_str)




def load_keys(filename="kay.txt"):
    keys = {}
    with open(filename, "r") as f:
        for line in f:
            index, value = line.strip().split(":")
            keys[int(index)] = int(value)
    return keys

keys = load_keys()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

try:
    while True:
        text = input("Enter text to send (or 'exit'): ")
        if text.lower() == "exit":
            break

        client.send(text.encode())

        data = client.recv(1024).decode()
        key_index_str, encrypted = data.split(":", 1)
        key_index = int(key_index_str)
        key_value = keys[key_index]

        decrypted = "".join(chr((ord(c) - key_value) % 256) for c in encrypted)
        print("Encrypted:", encrypted)
        print("Decrypted:", decrypted)

finally:
    client.close()
