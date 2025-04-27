# Detects opens that are open or responds 
import socket

def scan_ports(ip, ports=[21, 22, 80, 443, 8080], timeout=2):
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
    return open_ports