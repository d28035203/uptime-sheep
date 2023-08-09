#!/usr/bin/env python3
"""uptime-sheep — HTTP health checks with retries and JSON config."""
from __future__ import print_function

import argparse
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))


def check(url, timeout, retries):
    last_err = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                code = resp.getcode()
                if 200 <= code < 400:
                    return True, code, None
                last_err = "HTTP %s" % code
        except Exception as exc:
            last_err = str(exc)
        time.sleep(0.4 * (attempt + 1))
    return False, None, last_err


def main():
    parser = argparse.ArgumentParser(description="HTTP uptime checker")
    parser.add_argument("--once", action="store_true", help="single pass, exit 1 if any target fails")
    parser.add_argument("--config", default=os.path.join(HERE, "flock.json"))
    parser.add_argument("--interval", type=int, default=30, help="seconds between passes (loop mode)")
    args = parser.parse_args()

    with open(args.config) as fh:
        cfg = json.load(fh)
    timeout = cfg.get("timeout_sec", 5)
    retries = cfg.get("retries", 1)

    def run_round():
        failed = 0
        print("=== check %s ===" % time.strftime("%Y-%m-%d %H:%M:%S"))
        for target in cfg["targets"]:
            ok, code, err = check(target["url"], timeout, retries)
            if ok:
                print("[up]   %-16s %s" % (target["name"], code))
            else:
                failed += 1
                print("[down] %-16s %s" % (target["name"], err))
        return failed

    if args.once:
        return 1 if run_round() else 0

    while True:
        run_round()
        time.sleep(args.interval)


if __name__ == "__main__":
    sys.exit(main() or 0)
