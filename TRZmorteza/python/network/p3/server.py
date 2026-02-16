import socket
import struct
import re


ip_pattern = re.compile(r'^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}$')
port_pattern = re.compile(r'^\d{1,5}$')  # 0-65535

while not ip_pattern.match(HOST := input("Enter IP address: ")):
    print("Try again.")

while not port_pattern.match(port_str := input("Enter port: ")):
    print("Try again.")

PORT = int(port_str)

def recv_full(sock, size):
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5) 
print(f"Server listening on {HOST}:{PORT}...")

try:
    while True: 
        print("Waiting for a client to connect...")
        conn, addr = server.accept()
        print("Connected:", addr)

        try:
            while True:  
                raw_length = recv_full(conn, 4)
                if not raw_length:
                    print("Client disconnected.")
                    break

                message_length = struct.unpack('!I', raw_length)[0]
                data = recv_full(conn, message_length)
                if data is None:
                    print("Client disconnected mid-message.")
                    break

                conn.sendall(raw_length)
                conn.sendall(data)

        finally:
            conn.close()

        cmd = input("Type 'exit' to shut down server or press Enter to wait for next client: ")
        if cmd.lower() == 'exit':
            print("Shutting down server...")
            break

finally:
    server.close()
    print("Server closed.")
