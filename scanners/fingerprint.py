import subprocess

def fingerprint_os(ip):
    try:
        output = subprocess.check_output(["ping", "-c", "1", ip], timeout=3).decode()
        for line in output.splitlines():
            if "ttl=" in line.lower():
                ttl = int(line.lower().split("ttl=")[1].split()[0])
                if ttl <= 64:
                    return "Linux/Unix (TTL ~64)"
                elif ttl <= 128:
                    return "Windows (TTL ~128)"
                else:
                    return "Unknown OS (TTL={})".format(ttl)
    except:
        return "OS fingerprinting failed"
