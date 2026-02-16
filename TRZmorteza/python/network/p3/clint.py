import socket
import struct
import time
import re

ip_pattern = re.compile(r'^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}$')
port_pattern = re.compile(r'^\d{1,5}$')  

while not ip_pattern.match(HOST := input("Enter IP address: ")):
    print("Try again.")

while not port_pattern.match(PORT := input("Enter port: ")):
    print("Try again.")

ITERATIONS = 1000

def recv_full(sock, size):
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data

max_send=[1,2,4,8,16]
for i in max_send:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, int(PORT)))

    total_rtt = 0.0

    for _ in range(ITERATIONS):

        message = message = b'a' * (i * 1024)
    
        message_length = len(message)

        header = struct.pack('!I', message_length)

        start_time = time.perf_counter()

        client.sendall(header)
        client.sendall(message)

        raw_length = recv_full(client, 4)
        returned_length = struct.unpack('!I', raw_length)[0]

        data = recv_full(client, returned_length)

        end_time = time.perf_counter()

        total_rtt += (end_time - start_time)

    average_rtt = (total_rtt / ITERATIONS) * 1000
    sec=average_rtt*ITERATIONS/total_rtt

    print(f"Average RTT: {average_rtt:.6f} ms")
    print(f"sec: {sec} ms")

    client.close()
