import requests
import sys
import os
import time
from urllib.parse import urljoin

PAYLOAD_TYPES = ["xss", "rce", "lfi", "ssti"]
TIMEOUT = 10
HEADERS = {
    "User-Agent": "Mozilla/5.0 PentestPayloadEngine/1.0"
}
LOG_DIR = "attack_logs"

def load_payloads(payload_type):
    filename = f"payloads/{payload_type}.txt"
    if not os.path.exists(filename):
        print(f"[!] Missing payload file: {filename}")
        return []
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip() for line in f if line.strip()]

def save_log(payload_type, payload, status, content_snippet):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    with open(f"{LOG_DIR}/{payload_type}_log.txt", "a") as log:
        log.write(f"[{status}] {payload}\n")
        log.write(f"Response: {content_snippet[:300]}\n\n")

def test_payload(target, param, payload_type, payload):
    url = f"{target}?{param}={payload}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=TIMEOUT, verify=False)
        status = res.status_code
        content = res.text
        if payload.lower() in content.lower() or any(tag in content for tag in ["<script>", "uid=", "root:", "{{"]):
            print(f"[💥] Possible {payload_type.upper()} at {url}")
            save_log(payload_type, url, status, content)
        else:
            print(f"[.] Tried: {payload}")
    except Exception as e:
        print(f"[x] Error: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 payload_engine.py http://target.com/page.php?param=")
        sys.exit(1)

    target_url = sys.argv[1]
    if "?" not in target_url or "=" not in target_url:
        print("[!] Include parameter in URL, example: http://site.com/page?query=")
        sys.exit(1)

    base, param = target_url.split("?")[0], target_url.split("=")[0].split("?")[-1]

    for ptype in PAYLOAD_TYPES:
        print(f"\n[🔍] Testing {ptype.upper()} payloads...")
        payloads = load_payloads(ptype)
        for payload in payloads:
            test_payload(base, param, ptype, payload)

    print("\n✅ Done. Logs saved in attack_logs/")

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    main()