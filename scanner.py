import socket
import threading
import csv

def scan_host(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"[+] Port {port} is open on {host}")
            with open('open_ports.txt', 'a') as f:
                f.write(f"[+] Port {port} is open on {host}\n")
        sock.close()
    except Exception as e:
        print(f"[-] Error scanning port {port} on {host}: {str(e)}")

def scan_ports(hosts, ports):
    for host in hosts:
        for port in ports:
            t = threading.Thread(target=scan_host, args=(host, port))
            t.start()

if __name__ == '__main__':
    with open('domains.csv', 'r') as f:
        reader = csv.reader(f)
        subdomains = [row[1] for row in reader]

    #Define the port range to scan. Excluding ports 22, 80 and 443, because those need to be open.
    ports = [p for p in range(1, 65536) if p not in [22, 80, 443]]

    hosts = [f"{sub}" for sub in subdomains]
    scan_ports(hosts, ports)

