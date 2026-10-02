# Microsoft Clarity data pull

Pulls aggregated behaviour metrics for **thepawmisedland.com** from the Clarity
Data Export API, for funnel/conversion troubleshooting alongside Shopify data.

There is no Microsoft Clarity MCP connector in Claude's connector directory, so
this script is the route for reading Clarity data directly.

## Setup (one time)

Both of these live in the cloud environment's settings — the cloud environment
menu in the session title bar, then **Edit**:

1. **Network access** → add `www.clarity.ms` to the allowed domains.
   Note: `clarity.microsoft.com` is the *dashboard* host and is not sufficient;
   the API is served from `www.clarity.ms`.
2. **API credentials** (or environment variables) → add `CLARITY_API_TOKEN`.
   Generate the token in the Clarity dashboard under
   **Settings → Data Export**.

Changes are picked up by a newly started session.

## Usage

```bash
python3 tools/clarity/clarity_pull.py                        # today, no breakdown
python3 tools/clarity/clarity_pull.py --days 3               # 3 days (API max)
python3 tools/clarity/clarity_pull.py --dims URL             # per page
python3 tools/clarity/clarity_pull.py --dims Device,Browser  # up to 3 dimensions
```

Valid dimensions: `OS`, `Browser`, `Device`, `Country/Region`, `Source`,
`Medium`, `Campaign`, `Channel`, `URL`.

Raw JSON is written next to the script as `clarity_raw_<tag>.json`.

## Limits worth knowing

- **3 days maximum lookback.** History cannot be backfilled, so a bad day has
  to be pulled within 3 days of it happening.
- **10 requests per project per day.** Each call is scarce; pick dimensions
  deliberately rather than exploring one at a time.
- **Aggregated metrics only.** The API returns counts — dead clicks, rage
  clicks, excessive scroll, quickback clicks, script errors, engagement time,
  scroll depth, session and user counts. Session recordings and heatmaps are
  dashboard-only and are not exposed by this API.

## Most useful first calls

```bash
# Where friction is, by page — the highest-value single query
python3 tools/clarity/clarity_pull.py --days 1 --dims URL

# Whether friction is device- or browser-specific (store is ~90% mobile)
python3 tools/clarity/clarity_pull.py --days 1 --dims Device,Browser
```

## Caveat

The endpoint and parameter names were written without access to
`learn.microsoft.com` (blocked by the environment's network policy at the time).
If Microsoft has changed the contract, the script's error output names the
failing condition — token, quota, reachability, or HTTP status — which is enough
to correct it.
