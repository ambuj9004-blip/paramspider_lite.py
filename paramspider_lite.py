import requests
import sys
import re
from colorama import Fore, Style, init
from urllib.parse import urlparse

init(autoreset=True)

BANNER = """
██████╗  █████╗ ██████╗  █████╗ ███╗   ███╗
██╔══██╗██╔══██╗██╔══██╗██╔══██╗████╗ ████║
██████╔╝███████║██████╔╝███████║██╔████╔██║
██╔═══╝ ██╔══██║██╔══██╗██╔══██║██║╚██╔╝██║
██║     ██║  ██║██║  ██║██║  ██║██║ ╚═╝ ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
     ParamSpider Lite - By Ambuj Tiwari
     Bug Bounty | Penetration Testing
"""

def extract_params(url):
    print(Fore.CYAN + BANNER)
    
    try:
        parsed = urlparse(url)
        if not parsed.scheme:
            url = "https://" + url
            
        print(Fore.YELLOW + f"[*] Target: {url}")
        print(Fore.YELLOW + "[*] Fetching URL parameters...\n")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        r = requests.get(url, headers=headers, timeout=10, verify=False)
        
        # Extract all URLs with parameters
        pattern = r'https?://[^\s"\'<>]+\?[^\s"\'<>]+'
        urls_with_params = re.findall(pattern, r.text)
        
        if urls_with_params:
            print(Fore.GREEN + f"[+] Found {len(urls_with_params)} URLs with parameters:\n")
            seen = set()
            for u in urls_with_params:
                if u not in seen:
                    seen.add(u)
                    print(Fore.WHITE + f"  → {u}")
            
            # Save to file
            domain = urlparse(url).netloc
            filename = f"{domain}_params.txt"
            with open(filename, "w") as f:
                f.write("\n".join(seen))
            print(Fore.GREEN + f"\n[+] Results saved to: {filename}")
        else:
            print(Fore.RED + "[-] No parameters found on this page.")
            
        print(Fore.YELLOW + f"\n[*] Status Code: {r.status_code}")
        
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input(Fore.CYAN + "\nEnter Target URL: ")
    
    extract_params(url)
