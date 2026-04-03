<div align="center">

# 🕵️ OSINT-X — Automated Open Source Intelligence Tool

> **Aggregate public digital footprints and display results instantly in the terminal.**

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
- Displays a **clean, color-coded summary** directly in the terminal

Built as an educational cybersecurity portfolio project demonstrating real-world
reconnaissance workflows used in ethical penetration testing and threat intelligence.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔍 **Username Footprinting** | Checks presence on GitHub, Reddit, Twitter/X, Instagram, TikTok, Pinterest, Twitch, and HackerNews |
| 💥 **Breach Detection** | Integrates with HaveIBeenPwned API v3 to surface known credential leaks |
| 🎨 **Colored Terminal Output** | Clean, color-coded results with status indicators |
| ⚡ **Fast Concurrent Scanning** | Simultaneous HTTP checks via `ThreadPoolExecutor` |
| 🔒 **Privacy Respecting** | Only queries publicly accessible endpoints — no scraping, no auth bypass |

---

## 🛠️ Prerequisites

- Python 3.8+
- (Optional) A free API key from [HaveIBeenPwned](https://haveibeenpwned.com/API/Key) for breach checking

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

# 4. (Optional) Set your HaveIBeenPwned API key
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

### Full scan — username + email
```bash
python main.py --username target_user --email target@example.com
```

### All options
```
usage: main.py [-h] [--username USERNAME] [--email EMAIL]

options:
  -h, --help            Show this help message and exit
  --username USERNAME   Target username to footprint across platforms
  --email    EMAIL      Target email to check for data breaches
```

---

## 📋 Sample Output

```
[*] Scan started: 2026-04-03 11:35:34
[*] Scanning username: john_doe
------------------------------------------------------------
[+] GitHub         -> FOUND    (https://github.com/john_doe)
[+] Reddit         -> FOUND    (https://reddit.com/user/john_doe)
[-] Instagram      -> NOT FOUND
[-] Twitter/X      -> NOT FOUND
[+] TikTok         -> FOUND    (https://tiktok.com/@john_doe)

------------------------------------------------------------
  OSINT-X SCAN SUMMARY
------------------------------------------------------------
  Scan Time          : 2026-04-03 11:35:38
  Target Username    : john_doe

  [USERNAME FOOTPRINT]
  Platforms scanned  : 8
  Profiles found     : 3
  Not found          : 5

  Found on:
    [+] GitHub         https://github.com/john_doe
    [+] Reddit         https://reddit.com/user/john_doe
    [+] TikTok         https://tiktok.com/@john_doe
------------------------------------------------------------
```

---

## 📁 Project Structure

```
osint-x/
├── main.py              # Core application logic
├── requirements.txt     # Python dependencies
└── README.md            # This file
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
