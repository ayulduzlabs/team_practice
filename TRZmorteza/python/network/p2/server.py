import socket
import csv
from urllib.parse import unquote, parse_qs
import re

ip_pattern = re.compile(r'^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}$')
port_pattern = re.compile(r'^\d{1,5}$') 

while not ip_pattern.match(HOST := input("Enter IP address: ")):
    print("Try again.")

while not port_pattern.match(port_str := input("Enter port: ")):
    print("Try again.")

PORT = int(port_str)

CONTACTS_FILE = 'contacts.csv'

def load_contacts():
    contacts = []
    with open(CONTACTS_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            contacts.append(row)
    return contacts

contacts = load_contacts()

FORM_HTML = """
<html>
<head><title>Search Contact</title></head>
<body>
<h2>Search Contact</h2>
<form method="GET" action="/">
    Code: <input type="text" name="code"><br>
    Name: <input type="text" name="name"><br>
    Phone: <input type="text" name="phone"><br>
    Address: <input type="text" name="address"><br>
    Email: <input type="text" name="email"><br>
    <input type="submit" value="Search">
</form>
</body>
</html>
"""

def make_results_table(results):
    if not results:
        return "<h3>No results found!</h3>"
    table = "<table border='1' cellpadding='5'><tr><th>Code</th><th>Name</th><th>Phone</th><th>Address</th><th>Email</th></tr>"
    for c in results:
        table += f"<tr><td>{c['code']}</td><td>{c['name']}</td><td>{c['phone']}</td><td>{c['address']}</td><td>{c['email']}</td></tr>"
    table += "</table>"
    table += "<br><a href='/'>Back to search</a>"
    return table
def search_contacts(params):
    code = params.get('code', [''])[0].strip()
    name = params.get('name', [''])[0].strip().lower()
    phone = params.get('phone', [''])[0].strip()
    address = params.get('address', [''])[0].strip().lower()
    email = params.get('email', [''])[0].strip().lower()

    results = []

    if code:  
        for contact in contacts:
            if contact['code'] == code:
                return [contact]  
        return []  

    
    for contact in contacts:
        match = True
        if name and name not in contact['name'].lower():
            match = False
        if phone and phone not in contact['phone']:
            match = False
        if address and address not in contact['address'].lower():
            match = False
        if email and email not in contact['email'].lower():
            match = False
        if match:
            results.append(contact)

    return results

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server running on http://{HOST}:{PORT}")

try:
    while True:
        client_conn, client_addr = server_socket.accept()
        request = client_conn.recv(1024).decode('utf-8')
        if not request:
            client_conn.close()
            continue

        request_line = request.splitlines()[0]
        method, path, _ = request_line.split()

        if '?' in path:
            route, query_string = path.split('?', 1)
            params = parse_qs(unquote(query_string))
        else:
            route = path
            params = {}

        if params:
            results = search_contacts(params)
            body = make_results_table(results)
        else:
            body = FORM_HTML

        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + body
        client_conn.sendall(response.encode('utf-8'))
        client_conn.close()

finally:
    server_socket.close()
