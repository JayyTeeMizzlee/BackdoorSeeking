import argparse

def main():
    parser = argparse.ArgumentParser(prog="BackDoorSeeker", description="Vulnerability Scanner")
    parser.add_argument("--target", required=True, help="Target website or IP address")
    parser.add_argument("--scan", choices=["web", "ports", "both"], default="both", help="Select scan type")
    args = parser.parse_args()

    print(f"Starting {args.scan} scan on {args.target}...")

if __name__ == "__main__":
    main()
