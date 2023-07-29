#!/usr/bin/env python3
"""uptime-sheep — count HTTP sheep (health checks)."""
from __future__ import print_function
import argparse, json, os, sys, time, urllib.request

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
        except Exception as e:
            last_err = str(e)
        time.sleep(0.4 * (attempt + 1))
    return False, None, last_err

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--once", action="store_true")
    p.add_argument("--config", default=os.path.join(HERE, "flock.json"))
    args = p.parse_args()
    cfg = json.load(open(args.config))
    timeout = cfg.get("timeout_sec", 5)
    retries = cfg.get("retries", 1)

    def run_round():
        bad = 0
        print("=== uptime sheep %s ===" % time.strftime("%H:%M:%S"))
        for t in cfg["targets"]:
            ok, code, err = check(t["url"], timeout, retries)
            if ok:
                print("[awake] %-12s %s" % (t["name"], code))
            else:
                bad += 1
                print("[asleep] %-12s %s" % (t["name"], err))
        return bad

    if args.once:
        return 1 if run_round() else 0
    while True:
        run_round()
        time.sleep(30)

if __name__ == "__main__":
    sys.exit(main() or 0)
