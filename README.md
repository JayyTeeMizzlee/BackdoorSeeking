# BackdoorSeeking
The Backdoor Seeker is a lightweight vulnerability scanner designed to perform basic discovery and enumeration of a target system.
It currently scans for open TCP ports, grabs service banners, and attempts basic OS fingerprinting.

What can it currently do?
- Hostname Resolution: Converts domain names to IP addresses.
- TCP Port Scanning: Scans ports 1 to 1024 to find open services.
- Service Banner Grabbing: Connects to open ports and captures banners.
- Basic OS Fingerprinting: Estimates the operating system using TTL analysis.
- Command-Line Interface (CLI): Easy-to-use argument system.
- Web crawling for backdoor detection.
- Integration with Metasploit for automatic exploitation.
- Save scan results to JSON report files.

How to run this script (3 Steps)
- Step 1. 
        Open terminal.
- Step 2. 
        git clone https://github.com/yourusername/BackdoorSeeker.git
        cd BackdoorSeeker
- Step 3. 
        python3 -m venv venv
        source venv/bin/activate
- Step 4.
        pip install -r requirements.txt
        playwright install
- Step 5. 
        Running the script.
        Enter "python3 main.py --target scanme.nmap.org --scan (ports, web, or both)"

OPTIONAL
- To use the feature of exploit lookups please install the Metasploit Framework manually by using (bash/brew) install metasploit

FUTURE FEATURES
- N/A

Requirements
Python 3 and up.

Some legal testing targets
- scanme.nmap.org
- localhost