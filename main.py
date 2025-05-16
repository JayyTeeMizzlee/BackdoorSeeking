import json
import os
import datetime
import argparse
from scanners.host_resolver import resolve_hostname
from scanners.port_scanner import scan_ports
from scanners.banner_grabber import grab_banner
from scanners.fingerprint import fingerprint_os
from scanners.exploit_lookup import check_metasploit
from scanners.web_scanner import run_scrapy_scan, run_playwright_scan

def main():
    parser = argparse.ArgumentParser(prog="BackDoorSeeker", description="Vulnerability Scanner")
    parser.add_argument("--target", required=True, help="Target website or IP address")
    parser.add_argument("--scan", choices=["web", "ports", "both"], default="both", help="Select scan type")
    args = parser.parse_args()

# This is for JSON report structure
    os.makedirs("reports", exist_ok=True)
    scan_report = {
        "target": args.target,
        "ip": "",
        "os_fingerprint": "",
        "open_ports": [],
        "scrapy_results": {},
        "playwright_results": {}
    }

    print(f"Starting {args.scan} scan on {args.target}...")

    ip = resolve_hostname(args.target)
    if not ip:
        print ("This Target could not be resolved at this time.")
        return
    
    print(f"[+] Resolved IP: {ip}")
    scan_report["ip"] = ip

    print(f"[+] Attempting OS fingerprinting...")
    assumed_os = fingerprint_os(ip)
    print(f"[+] Operating System: {assumed_os}")
    scan_report["os_fingerprint"] = assumed_os

# Ports
    if args.scan in ("ports", "both"):
    
        test_ports = list(range(1, 1025))  

        print(f"[+] Scanning ports 1 to 1024...")
        open_ports = scan_ports(ip, ports=test_ports)
    
        if open_ports:
            print(f"[+] Open Ports Found: {open_ports}")
            for port in open_ports:
                port_info = {"port": port}
                banner = grab_banner(ip, port)
                if banner:
                    print(f"[Port {port}] Banner: {banner}")
                    port_info["banner"] = banner
                    service = banner.lower().split("-")[0].split("/")[0].strip()
                    exploits = check_metasploit(service)
                    port_info["metasploit_exploits"] = exploits
                    if exploits:
                        print(f"[+] Metasploit results for '{service}':")
                        for e in exploits:
                            print(f"    - {e}")
                else:
                    print(f"[Port {port}] No banner retrieved.")
                    port_info["banner"] = None
                    port_info["metasploit_exploits"] = []

                scan_report["open_ports"].append(port_info)
        else:
            print("[-] No open ports detected.")

# Web
    if args.scan in ("web", "both"):
        
        # Scrapy's Scan
        print("\n[+] Starting static web scan...")
        scrapy_results = run_scrapy_scan(f"http://{args.target}")
        print(f"[+] Scrapy: {len(scrapy_results['urls'])} URLs found")
        for s in scrapy_results["suspicious"]:
            print(f"[!] Scrapy Suspicious Path: {s}")

        scan_report["scrapy_results"] = {
            "total_urls": len(scrapy_results["urls"]),
            "suspicious": scrapy_results["suspicious"]
        }

        # Playwrights scan
        print("\n[+] Starting dynamic web scan...")
        playwright_results = run_playwright_scan(f"http://{args.target}")
        print(f"[+] Playwright: {len(playwright_results['dynamic_urls'])} URLs found")
        for s in playwright_results["suspicious"]:
            print(f"[!] Playwright Suspicious Path: {s}")

        scan_report["playwright_results"] = {
            "total_urls": len(playwright_results["dynamic_urls"]),
            "suspicious": playwright_results["suspicious"]
        }

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join("reports", f"scan_results_{timestamp}.json")
        with open(filename, "w") as f:
            json.dump(scan_report, f, indent=4)
        print(f"\n[+] Scan report saved to {filename}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[ ] Now Leaving scan..")
