import nmap

def scan_ports(target,ports):
    net_map = nmap.PortScanner()
    string = []

    for i in ports:
        string.append(str(i))
    
    port_string = ','.join(string)
    print(port_string)

    print(f"[*] Scanning ports on {target} ====> {port_string}")
    net_map.scan(hosts=target, ports=port_string)

    re