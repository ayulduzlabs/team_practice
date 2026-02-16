import socket
import random
import re

# Regex
ip_pattern = re.compile(r'^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}$')
port_pattern = re.compile(r'^\d{1,5}$')  # 0-65535

while not ip_pattern.match(HOST := input("Enter IP address: ")):
    print("Try again.")

while not port_pattern.match(PORT := input("Enter port: ")):
    print("Try again.")


def load_keys(filename="kay.txt"):
    keys = {}
    with open(filename, "r") as f:
        for line in f:
            index, value = line.strip().split(":")
            keys[int(index)] = int(value)
    return keys

keys = load_keys()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, int(PORT)))
server.listen(1)
print(f"Server listening on {HOST}:{PORT}")

conn, addr = server.accept()
print("Connected:", addr)

try:
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        data_upper = data.upper()

        key_index = random.randint(0, 9)
        key_value = keys[key_index]

        encrypted = "".join(chr((ord(c) + key_value) % 256) for c in data_upper)

        message = f"{key_index}:{encrypted}"
        conn.send(message.encode())

finally:
    conn.close()
    server.close()
    print("Server closed.")
