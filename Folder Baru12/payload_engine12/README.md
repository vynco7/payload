# Payload Engine - Ultimate Auto Attack Tool 

## 🚀 Description
This tool automatically tests a given URL with thousands of payloads for:
- XSS
- RCE
- LFI
- SSTI

## ⚡ How to Use

```bash
python3 payload_engine.py "http://target.com/page.php?param="
```

**Example:**

```bash
python3 payload_engine.py "http://victim.com/index.php?q="
```

## 💣 Features

- Loop thousands of payloads
- Auto detect possible vulnerability
- Save logs to `attack_logs/`
- Includes basic payload wordlists in `payloads/` folder

## 🧨 Requirements

- Python 3.x
- requests library

## ⚠️ Disclaimer

This tool is for educational and authorized penetration testing **only**.  
Using it without permission may be illegal.

---

Created by vynco
