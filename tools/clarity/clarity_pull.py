#!/usr/bin/env python3
"""
Microsoft Clarity Data Export API client for thepawmisedland.com.

Usage:
    python3 clarity_pull.py                         # today, no breakdown
    python3 clarity_pull.py --days 3                # last 3 days (API max)
    python3 clarity_pull.py --dims URL              # break down by page
    python3 clarity_pull.py --dims Device,Browser   # up to 3 dimensions

Requires CLARITY_API_TOKEN in the environment.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

ENDPOINT = "https://www.clarity.ms/export-data/api/v1/project-live-insights"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Dimensions the API accepts (max 3 per request).
VALID_DIMS = [
    "OS", "Browser", "Device", "Country/Region",
    "Source", "Medium", "Campaign", "Channel", "URL",
]


def fetch(token, num_days, dims):
    params = [("numOfDays", str(num_days))]
    for i, d in enumerate(dims, start=1):
        params.append((f"dimension{i}", d))
    url = f"{ENDPOINT}?{urllib.parse.urlencode(params)}"

    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8")), url
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:500]
        if e.code == 401:
            die("401 Unauthorized — the token is wrong, expired, or from another "
                "Clarity project.\nRegenerate it: Clarity dashboard → Settings → "
                "Data Export.")
        if e.code == 403:
            die("403 Forbidden — the token lacks access to this project, or data "
                "export is not enabled on it.")
        if e.code == 429:
            die("429 Rate limited — the Clarity API allows only 10 requests per "
                "project per day. Wait for the quota to reset.")
        die(f"HTTP {e.code} from Clarity.\n{body}")
    except urllib.error.URLError as e:
        die(f"Could not reach www.clarity.ms ({e.reason}).\n"
            "The environment's network policy is still blocking it. Add "
            "'www.clarity.ms' to the allowed domains, then start a new session.")


def die(msg):
    print(f"\nFAILED: {msg}\n", file=sys.stderr)
    sys.exit(1)


def render(payload, num_days, dims):
    """Clarity returns a list of {metricName, information:[{...}]} objects."""
    if not isinstance(payload, list):
        print("Unexpected payload shape; dumping raw:")
        print(json.dumps(payload, indent=2)[:4000])
        return

    scope = f"last {num_days} day(s)"
    if dims:
        scope += f", broken down by {' / '.join(dims)}"
    print(f"\nMicrosoft Clarity — {scope}")
    print("=" * 72)

    for metric in payload:
        name = metric.get("metricName", "(unnamed)")
        rows = metric.get("information") or []
        print(f"\n{name}")
        print("-" * len(name))
        if not rows:
            print("  (no data)")
            continue
        for row in rows:
            # Separate the dimension labels from the measures.
            labels = {k: v for k, v in row.items() if k in dims}
            measures = {k: v for k, v in row.items() if k not in dims}
            prefix = "  "
            if labels:
                prefix += " | ".join(f"{k}={v}" for k, v in labels.items()) + "  →  "
            print(prefix + ", ".join(f"{k}: {v}" for k, v in measures.items()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=1,
                    help="1-3. The API cannot look back further than 3 days.")
    ap.add_argument("--dims", default="",
                    help=f"Comma-separated, max 3. Options: {', '.join(VALID_DIMS)}")
    args = ap.parse_args()

    if not 1 <= args.days <= 3:
        die("--days must be 1, 2 or 3 (Clarity's API maximum lookback is 3 days).")

    dims = [d.strip() for d in args.dims.split(",") if d.strip()]
    if len(dims) > 3:
        die("At most 3 dimensions per request.")
    bad = [d for d in dims if d not in VALID_DIMS]
    if bad:
        die(f"Unknown dimension(s): {', '.join(bad)}\nValid: {', '.join(VALID_DIMS)}")

    token = os.environ.get("CLARITY_API_TOKEN", "").strip()
    if not token:
        die("CLARITY_API_TOKEN is not set.\nAdd it in the environment's settings "
            "(cloud environment menu in the session title bar → Edit → API "
            "credentials), then start a new session.")

    payload, url = fetch(token, args.days, dims)

    tag = f"{args.days}d" + (("_" + "_".join(dims).replace("/", "-")) if dims else "")
    raw_path = os.path.join(OUT_DIR, f"clarity_raw_{tag}.json")
    with open(raw_path, "w") as fh:
        json.dump(payload, fh, indent=2)

    render(payload, args.days, dims)
    print(f"\nRaw JSON saved to: {raw_path}")


if __name__ == "__main__":
    main()
