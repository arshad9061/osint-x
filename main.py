"""
OSINT-X — Automated Open Source Intelligence Report Generator
=============================================================
Author  : Your Name
Version : 1.0.0
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
from fpdf import FPDF
from colorama import Fore, Style, init

# ── Initialize colorama for cross-platform color support ──────────────────────
init(autoreset=True)

# ── Constants ─────────────────────────────────────────────────────────────────
HIBP_API_KEY = os.environ.get("HIBP_API_KEY", "")
HIBP_BASE_URL = "https://haveibeenpwned.com/api/v3"
TIMEOUT = 8  # seconds per HTTP request

# ── Platform definitions: name → profile URL template ─────────────────────────
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

# ── Helpers ───────────────────────────────────────────────────────────────────

def banner():
    """Print a styled ASCII banner."""
    print(Fore.CYAN + Style.BRIGHT + r"""
  ___  ____  ___ _   _ _____      __  __
 / _ \/ ___|_ _| \ | |_   _|_   _\ \/ /
| | | \___ \| ||  \| | | | \ \ / /\  / 
| |_| |___) | || |\  | | |  \ V / /  \ 
 \___/|____/___|_| \_| |_|   \_/ /_/\_\
    """ + Style.RESET_ALL)
    print(Fore.YELLOW + "  Automated OSINT Report Generator | Educational Use Only\n")


def log(msg: str, level: str = "info"):
    """Color-coded terminal logging."""
    icons = {
        "info":    (Fore.CYAN,   "[*]"),
        "found":   (Fore.GREEN,  "[+]"),
        "missing": (Fore.RED,    "[-]"),
        "warn":    (Fore.YELLOW, "[!]"),
        "success": (Fore.GREEN,  "[✔]"),
        "error":   (Fore.RED,    "[✘]"),
    }
    color, icon = icons.get(level, (Fore.WHITE, "[?]"))
    print(f"{color}{icon} {msg}{Style.RESET_ALL}")


# ── Module 1: Username Platform Footprinting ──────────────────────────────────

def check_platform(platform: str, url: str) -> dict:
    """
    Check if a username profile URL returns HTTP 200.
    Returns a result dict with platform, url, and found status.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; OSINT-X/1.0)"}
        response = requests.get(url, headers=headers, timeout=TIMEOUT, allow_redirects=True)
        found = response.status_code == 200
        return {"platform": platform, "url": url, "found": found, "status": response.status_code}
    except requests.RequestException as e:
        return {"platform": platform, "url": url, "found": False, "status": f"Error: {e}"}


def scan_username(username: str) -> list:
    """
    Concurrently probe all defined platforms for the given username.
    Returns a list of result dicts.
    """
    log(f"Scanning username: {Fore.WHITE + Style.BRIGHT}{username}", "info")
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(check_platform, name, url.format(username)): name
            for name, url in PLATFORMS.items()
        }
        for future in as_completed(futures):
            result = future.result()
            if result["found"]:
                log(f"{result['platform']:<14} → FOUND    {Fore.WHITE}({result['url']})", "found")
            else:
                log(f"{result['platform']:<14} → NOT FOUND", "missing")
            results.append(result)

    # Sort alphabetically for consistent report ordering
    return sorted(results, key=lambda r: r["platform"])


# ── Module 2: Email Breach Detection (HaveIBeenPwned) ─────────────────────────

def check_breaches(email: str) -> list:
    """
    Query the HaveIBeenPwned API v3 for breaches associated with an email.
    Requires HIBP_API_KEY to be set in the environment.
    Returns a list of breach dicts, or an empty list.
    """
    log(f"Checking breaches for: {Fore.WHITE + Style.BRIGHT}{email}", "info")

    if not HIBP_API_KEY:
        log("HIBP_API_KEY not set. Skipping breach check. Export it as an env variable.", "warn")
        return []

    url = f"{HIBP_BASE_URL}/breachedaccount/{email}"
    headers = {
        "hibp-api-key": HIBP_API_KEY,
        "User-Agent":   "OSINT-X-Tool",
    }
    params = {"truncateResponse": "false"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)

        if response.status_code == 200:
            breaches = response.json()
            for b in breaches:
                data_classes = ", ".join(b.get("DataClasses", []))
                log(
                    f"BREACH: {b['Name']} ({b.get('BreachDate','?')}) — "
                    f"{b.get('PwnCount', '?'):,} accounts — "
                    f"Exposed: {data_classes}",
                    "warn"
                )
            return breaches

        elif response.status_code == 404:
            log("No breaches found for this email address.", "found")
            return []

        elif response.status_code == 401:
            log("HIBP API key is invalid or unauthorized.", "error")
            return []

        elif response.status_code == 429:
            log("HIBP rate limit hit. Wait 1-2 seconds and retry.", "error")
            return []

        else:
            log(f"Unexpected HIBP response: HTTP {response.status_code}", "error")
            return []

    except requests.RequestException as e:
        log(f"Network error during breach check: {e}", "error")
        return []


# ── Module 3: PDF Report Generation ──────────────────────────────────────────

class OSINTReport(FPDF):
    """Custom FPDF subclass with branded header and footer."""

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, "OSINT-X - Intelligence Report", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(200, 0, 0)
        self.set_line_width(0.5)
        self.line(10, 22, 200, 22)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"OSINT-X | For Authorized Research Only | Page {self.page_no()}", align="C")

    def section_title(self, title: str):
        """Render a colored section heading."""
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(30, 30, 30)
        self.cell(0, 8, f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def key_value_row(self, key: str, value: str, color: tuple = (0, 0, 0)):
        """Render a labeled data row."""
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(80, 80, 80)
        self.cell(50, 7, key)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*color)
        # Calculate remaining width explicitly to avoid fpdf2 multi_cell width=0 bug
        remaining = self.w - self.r_margin - self.get_x()
        self.multi_cell(remaining, 7, value)


def generate_pdf_report(
    username,
    email,
    platform_results: list,
    breach_results: list,
    output_dir: str = ".",
) -> str:
    """
    Compile all scan results into a structured PDF report.
    Returns the path to the saved PDF.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_label = username or (email.split("@")[0] if email else "unknown")
    filename = f"osint_report_{target_label}_{timestamp}.pdf"
    filepath = os.path.join(output_dir, filename)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    pdf = OSINTReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ── Meta Section ──────────────────────────────────────────────────────────
    pdf.section_title("Scan Metadata")
    pdf.key_value_row("Generated     :", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    pdf.key_value_row("Tool          :", "OSINT-X v1.0.0")
    if username:
        pdf.key_value_row("Target User   :", username)
    if email:
        pdf.key_value_row("Target Email  :", email)
    pdf.key_value_row("Disclaimer    :", "For authorized research and educational use only.")
    pdf.ln(4)

    # ── Platform Results ──────────────────────────────────────────────────────
    if platform_results:
        pdf.section_title("Username Footprinting Results")
        found_count = sum(1 for r in platform_results if r["found"])
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 6, f"  Scanned {len(platform_results)} platforms - {found_count} profile(s) found.", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        for result in platform_results:
            if result["found"]:
                pdf.key_value_row(f"  {result['platform']}", result["url"], color=(0, 128, 0))
            else:
                pdf.key_value_row(f"  {result['platform']}", "Not Found", color=(180, 0, 0))
        pdf.ln(4)

    # ── Breach Results ────────────────────────────────────────────────────────
    if email:
        pdf.section_title("Data Breach Check Results")
        if breach_results:
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(180, 0, 0)
            pdf.cell(0, 6, f"  {len(breach_results)} breach(es) found for {email}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)

            for breach in breach_results:
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(30, 30, 30)
                pdf.cell(0, 7, f"  Breach: {breach.get('Name', 'Unknown')}", new_x="LMARGIN", new_y="NEXT")

                pdf.set_font("Helvetica", "", 9)
                pdf.set_text_color(80, 80, 80)
                pdf.cell(55, 6, "    Date:")
                pdf.cell(0, 6, breach.get("BreachDate", "Unknown"), new_x="LMARGIN", new_y="NEXT")

                pdf.cell(55, 6, "    Accounts Exposed:")
                pdf.cell(0, 6, f"{breach.get('PwnCount', 0):,}", new_x="LMARGIN", new_y="NEXT")

                data_classes = ", ".join(breach.get("DataClasses", []))
                pdf.cell(55, 6, "    Data Compromised:")
                pdf.multi_cell(0, 6, data_classes)
                pdf.ln(2)
        elif not HIBP_API_KEY:
            pdf.key_value_row("  Status:", "Skipped - HIBP_API_KEY not configured.", color=(150, 100, 0))
        else:
            pdf.key_value_row("  Status:", "No breaches found for this email address.", color=(0, 128, 0))
        pdf.ln(4)

    # ── Legal Notice ──────────────────────────────────────────────────────────
    pdf.section_title("Legal Notice")
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(
        0, 6,
        "This report was generated by OSINT-X for authorized educational or security research "
        "purposes only. All data sourced from publicly available information. Unauthorized use "
        "against individuals or systems without explicit consent is illegal and unethical."
    )

    pdf.output(filepath)
    return filepath


# ── CLI Entry Point ───────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        prog="osint-x",
        description="OSINT-X: Automated Open Source Intelligence Report Generator",
        epilog="Example: python main.py --username johndoe --email john@example.com",
    )
    parser.add_argument("--username", "-u", type=str, help="Target username to footprint")
    parser.add_argument("--email",    "-e", type=str, help="Target email to check for breaches")
    parser.add_argument(
        "--output", "-o", type=str, default=".",
        help="Output directory for the PDF report (default: current directory)"
    )
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

    # ── Username scan ─────────────────────────────────────────────────────────
    if args.username:
        platform_results = scan_username(args.username)
        print()

    # ── Email breach check ────────────────────────────────────────────────────
    if args.email:
        breach_results = check_breaches(args.email)
        print()

    # ── Generate report ───────────────────────────────────────────────────────
    log("Compiling PDF report...", "info")
    report_path = generate_pdf_report(
        username=args.username,
        email=args.email,
        platform_results=platform_results,
        breach_results=breach_results,
        output_dir=args.output,
    )

    log(f"PDF Report saved → {Fore.WHITE + Style.BRIGHT}{report_path}", "success")
    print()


if __name__ == "__main__":
    main()
