"""
OSINT-X -- Automated Open Source Intelligence Tool
===================================================
Author  : Your Name
Version : 1.1.0
Purpose : Educational OSINT tool for authorized security research only.

DISCLAIMER: Use only on yourself or with explicit written consent.
Unauthorized use may violate CFAA, GDPR, or laws in your jurisdiction.
"""

import os
import sys
import argparse
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init

# -- Initialize colorama for cross-platform color support ---------------------
init(autoreset=True)

# -- Constants ----------------------------------------------------------------
HIBP_API_KEY = os.environ.get("HIBP_API_KEY", "")
HIBP_BASE_URL = "https://haveibeenpwned.com/api/v3"
TIMEOUT = 8  # seconds per HTTP request

# -- Platform definitions: name -> profile URL template ----------------------
PLATFORMS = {
    "GitHub":      "https://github.com/{}",
    "Reddit":      "https://www.reddit.com/user/{}",
    "Twitter/X":   "https://twitter.com/{}",
    "Instagram":   "https://www.instagram.com/{}",
    "TikTok":      "https://www.tiktok.com/@{}",
    "Pinterest":   "https://www.pinterest.com/{}/",
    "Twitch":      "https://www.twitch.tv/{}",
    "HackerNews":  "https://news.ycombinator.com/user?id={}",
}

# -- Helpers ------------------------------------------------------------------

def banner():
    print(Fore.CYAN + Style.BRIGHT + r"""
  ___  ____  ___ _   _ _____      __  __
 / _ \/ ___|_ _| \ | |_   _|_   _\ \/ /
| | | \___ \| ||  \| | | | \ \ / /\  / 
| |_| |___) | || |\  | | |  \ V / /  \ 
 \___/|____/___|_| \_| |_|   \_/ /_/\_\
    """ + Style.RESET_ALL)
    print(Fore.YELLOW + "  Automated OSINT Tool | Educational Use Only\n")


def log(msg, level="info"):
    icons = {
        "info":    (Fore.CYAN,   "[*]"),
        "found":   (Fore.GREEN,  "[+]"),
        "missing": (Fore.RED,    "[-]"),
        "warn":    (Fore.YELLOW, "[!]"),
        "success": (Fore.GREEN,  "[OK]"),
        "error":   (Fore.RED,    "[X]"),
    }
    color, icon = icons.get(level, (Fore.WHITE, "[?]"))
    print(f"{color}{icon} {msg}{Style.RESET_ALL}")


def print_divider():
    print(Fore.CYAN + "-" * 60 + Style.RESET_ALL)


# -- Module 1: Username Platform Footprinting ---------------------------------

def check_platform(platform, url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; OSINT-X/1.0)"}
        response = requests.get(url, headers=headers, timeout=TIMEOUT, allow_redirects=True)
        found = response.status_code == 200
        return {"platform": platform, "url": url, "found": found, "status": response.status_code}
    except requests.RequestException as e:
        return {"platform": platform, "url": url, "found": False, "status": str(e)}


def scan_username(username):
    log(f"Scanning username: {Fore.WHITE + Style.BRIGHT}{username}", "info")
    print_divider()
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(check_platform, name, url.format(username)): name
            for name, url in PLATFORMS.items()
        }
        for future in as_completed(futures):
            result = future.result()
            if result["found"]:
                log(f"{result['platform']:<14} -> FOUND    ({result['url']})", "found")
            else:
                log(f"{result['platform']:<14} -> NOT FOUND", "missing")
            results.append(result)

    return sorted(results, key=lambda r: r["platform"])


# -- Module 2: Email Breach Detection ----------------------------------------

def check_breaches(email):
    log(f"Checking breaches for: {Fore.WHITE + Style.BRIGHT}{email}", "info")
    print_divider()

    if not HIBP_API_KEY:
        log("HIBP_API_KEY not set. Skipping breach check.", "warn")
        return []

    url = f"{HIBP_BASE_URL}/breachedaccount/{email}"
    headers = {"hibp-api-key": HIBP_API_KEY, "User-Agent": "OSINT-X-Tool"}
    params = {"truncateResponse": "false"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)

        if response.status_code == 200:
            breaches = response.json()
            for b in breaches:
                data_classes = ", ".join(b.get("DataClasses", []))
                log(
                    f"BREACH: {b['Name']} ({b.get('BreachDate', '?')}) "
                    f"| {b.get('PwnCount', '?'):,} accounts "
                    f"| Exposed: {data_classes}",
                    "warn"
                )
            return breaches
        elif response.status_code == 404:
            log("No breaches found for this email.", "found")
            return []
        elif response.status_code == 401:
            log("HIBP API key is invalid or unauthorized.", "error")
            return []
        elif response.status_code == 429:
            log("HIBP rate limit hit. Try again later.", "error")
            return []
        else:
            log(f"Unexpected HIBP response: HTTP {response.status_code}", "error")
            return []

    except requests.RequestException as e:
        log(f"Network error: {e}", "error")
        return []


# -- Module 3: Terminal Summary -----------------------------------------------

def print_summary(username, email, platform_results, breach_results):
    print()
    print_divider()
    print(Fore.CYAN + Style.BRIGHT + "  OSINT-X SCAN SUMMARY" + Style.RESET_ALL)
    print_divider()
    print(f"  {'Scan Time':<18}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if username:
        print(f"  {'Target Username':<18}: {username}")
    if email:
        print(f"  {'Target Email':<18}: {email}")
    print()

    if platform_results:
        found     = [r for r in platform_results if r["found"]]
        not_found = [r for r in platform_results if not r["found"]]
        print(Fore.CYAN + "  [USERNAME FOOTPRINT]" + Style.RESET_ALL)
        print(f"  Platforms scanned : {len(platform_results)}")
        print(f"  Profiles found    : {Fore.GREEN}{len(found)}{Style.RESET_ALL}")
        print(f"  Not found         : {Fore.RED}{len(not_found)}{Style.RESET_ALL}")
        if found:
            print()
            print(Fore.GREEN + "  Found on:" + Style.RESET_ALL)
            for r in found:
                print(f"    [+] {r['platform']:<14} {r['url']}")
        print()

    if email:
        print(Fore.CYAN + "  [BREACH CHECK]" + Style.RESET_ALL)
        if breach_results:
            print(f"  {Fore.YELLOW}Breaches found: {len(breach_results)}{Style.RESET_ALL}")
            for b in breach_results:
                print(f"    [!] {b.get('Name')} ({b.get('BreachDate','?')}) - {b.get('PwnCount',0):,} accounts")
        elif HIBP_API_KEY:
            print(f"  {Fore.GREEN}No breaches found.{Style.RESET_ALL}")
        else:
            print(f"  {Fore.YELLOW}Skipped - HIBP_API_KEY not set.{Style.RESET_ALL}")

    print()
    print_divider()


# -- CLI Entry Point ----------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        prog="osint-x",
        description="OSINT-X: Automated Open Source Intelligence Tool",
        epilog="Example: python main.py --username johndoe --email john@example.com",
    )
    parser.add_argument("--username", "-u", type=str, help="Target username to footprint")
    parser.add_argument("--email",    "-e", type=str, help="Target email to check for breaches")
    return parser.parse_args()


def main():
    banner()
    args = parse_args()

    if not args.username and not args.email:
        log("Provide at least --username or --email. Use -h for help.", "error")
        sys.exit(1)

    log(f"Scan started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "info")
    print()

    platform_results = []
    breach_results   = []

    if args.username:
        platform_results = scan_username(args.username)
        print()

    if args.email:
        breach_results = check_breaches(args.email)
        print()

    print_summary(args.username, args.email, platform_results, breach_results)


if __name__ == "__main__":
    main()
