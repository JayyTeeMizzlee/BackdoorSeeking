# Attempts to read the service banner of each port it find open                   
import socket

def grab_banner(ip, port, timeout=2):
    try:
        with socket.socket() as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            banner = s.recv(1024).decode(errors="ignore").strip()
            return banner
    except:
        return None
