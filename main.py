import argparse
from scanners.host_resolver import resolve_hostname
from scanners.port_scanner import scan_ports
from scanners.banner_grabber import grab_banner
from scanners.fingerprint import fingerprint_os
from scanners.web_scanner import run_scrapy_scan, run_playwright_scan

def main():
    parser = argparse.ArgumentParser(prog="BackDoorSeeker", description="Vulnerability Scanner")
    parser.add_argument("--target", required=True, help="Target website or IP address")
    parser.add_argument("--scan", choices=["web", "ports", "both"], default="both", help="Select scan type")
    args = parser.parse_args()

    print(f"Starting {args.scan} scan on {args.target}...")

    ip = resolve_hostname(args.target)
    if not ip:
        print ("This Target could not be resolved at this time.")
        return
    
    print(f"[+] Resolved IP: {ip}")

    print(f"[+] Attempting OS fingerprinting...")
    assumed_os = fingerprint_os(ip)
    print(f"[+] Operating System: {assumed_os}")


    if args.scan in ("ports", "both"):
    
        test_ports = list(range(1, 1025))  

        print(f"[+] Scanning ports 1 to 1024...")
        open_ports = scan_ports(ip, ports=test_ports)
    
        if open_ports:
            print(f"[+] Open Ports Found: {open_ports}")
            for port in open_ports:
                banner = grab_banner(ip, port)
                if banner:
                    print(f"[Port {port}] Banner: {banner}")
                else:
                    print(f"[Port {port}] No banner retrieved.")
        else:
            print("[-] No open ports detected.")

    if args.scan in ("web", "both"):
        
        # Scrapy's Scan
        print("\n[+] Starting static web scan...")
        scrapy_results = run_scrapy_scan(f"http://{args.target}")
        print(f"[+] Scrapy: {len(scrapy_results['urls'])} URLs found")
        for s in scrapy_results["suspicious"]:
            print(f"[!] Scrapy Suspicious Path: {s}")

        # Playwrights scan
        print("\n[+] Starting dynamic web scan...")
        playwright_results = run_playwright_scan(f"http://{args.target}")
        print(f"[+] Playwright: {len(playwright_results['dynamic_urls'])} URLs found")
        for s in playwright_results["suspicious"]:
            print(f"[!] Playwright Suspicious Path: {s}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[ ] Now Leaving scan..")
