#!/usr/bin/env python3
import json
import sys
import urllib.error
import urllib.request


TIMEOUT = 5


def fetch_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
        return response.read().decode("utf-8").strip()


def get_egress_ip() -> str:
    try:
        data = json.loads(fetch_text("https://api.ipify.org?format=json"))
        ip = data.get("ip", "").strip()
        if ip:
            return ip
    except (OSError, ValueError, json.JSONDecodeError, urllib.error.URLError):
        pass

    try:
        ip = fetch_text("https://ifconfig.me/ip")
        if ip:
            return ip
    except (OSError, urllib.error.URLError):
        pass

    raise RuntimeError("Unable to determine egress IP")


def main() -> int:
    try:
        print(f"Current egress IP: {get_egress_ip()}")
        return 0
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
