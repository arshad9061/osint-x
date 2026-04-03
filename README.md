<div align="center">

# 🕵️ OSINT-X — Automated Open Source Intelligence Tool

> **Aggregate public digital footprints and generate professional PDF reports in seconds.**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![OSINT](https://img.shields.io/badge/Category-OSINT-red?style=for-the-badge)

</div>

---

## 📌 Overview

**OSINT-X** is a command-line OSINT (Open Source Intelligence) tool built in Python.
It accepts a **username** or **email address** and automatically:

- Probes **public platform profiles** across 8+ major sites
- Queries the **HaveIBeenPwned API** for known data breaches
- Compiles all findings into a **clean, timestamped PDF report**

Built as an educational cybersecurity portfolio project demonstrating real-world
reconnaissance workflows used in ethical penetration testing and threat intelligence.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔍 **Username Footprinting** | Checks presence on GitHub, Reddit, Twitter/X, Instagram, TikTok, Pinterest, Twitch, and HackerNews |
| 💥 **Breach Detection** | Integrates with HaveIBeenPwned API v3 to surface known credential leaks |
| 📄 **PDF Report Generation** | Auto-generates a structured, timestamped PDF with all findings |
| 🎨 **Colored CLI Output** | Rich terminal output with color-coded status indicators |
| ⚡ **Fast Concurrent Scanning** | Concurrent HTTP checks via `ThreadPoolExecutor` |
| 🔒 **Privacy Respecting** | Only queries publicly accessible endpoints — no scraping, no auth bypass |

---

## 🛠️ Prerequisites

- Python 3.8+
- A free API key from [HaveIBeenPwned](https://haveibeenpwned.com/API/Key)

---

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/osint-x.git
cd osint-x

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your HaveIBeenPwned API key
export HIBP_API_KEY="your_api_key_here"   # Windows: set HIBP_API_KEY=your_api_key_here
```

---

## 💻 Usage

### Scan by Username
```bash
python main.py --username target_user
```

### Scan by Email (breach check)
```bash
python main.py --email target@example.com
```

### Full scan (username + email) with custom output path
```bash
python main.py --username target_user --email target@example.com --output ./reports/
```

### All options
```
usage: main.py [-h] [--username USERNAME] [--email EMAIL] [--output OUTPUT]

options:
  -h, --help            Show this help message and exit
  --username USERNAME   Target username to footprint across platforms
  --email EMAIL         Target email to check for data breaches
  --output OUTPUT       Output directory for the PDF report (default: current dir)
```

---

## 📋 Sample Terminal Output

```
[*] Scan started: 2025-06-10 14:32:01
[*] Target Username : john_doe
[*] Target Email    : john@example.com

[+] GitHub          → FOUND   (https://github.com/john_doe)
[+] Reddit          → FOUND   (https://reddit.com/user/john_doe)
[-] Instagram       → NOT FOUND
[-] Twitter/X       → NOT FOUND
[+] TikTok          → FOUND   (https://tiktok.com/@john_doe)

[*] Checking breaches for john@example.com...
[!] BREACH: Adobe (2013) — 153,000,000 accounts — Email, Password, Username
[!] BREACH: LinkedIn (2016) — 164,000,000 accounts — Email, Password

[✔] PDF Report saved → osint_report_john_doe_20250610_143205.pdf
```

---

## 📁 Project Structure

```
osint-x/
├── main.py              # Core application logic
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── reports/             # Generated PDF reports (auto-created)
```

---

## ⚠️ Ethical & Legal Disclaimer

> **This tool is intended strictly for educational purposes and authorized security research.**
>
> - ✅ Use only on yourself or with **explicit written consent** from the target.
> - ✅ Ensure compliance with all applicable local, national, and international laws.
> - ❌ Do **NOT** use this tool for stalking, harassment, or unauthorized surveillance.
> - ❌ The author bears **no responsibility** for any misuse of this software.
>
> Unauthorized use of OSINT tools may violate the **Computer Fraud and Abuse Act (CFAA)**,
> **GDPR**, or equivalent legislation in your jurisdiction.

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
Made for educational purposes | Use responsibly
</div>
