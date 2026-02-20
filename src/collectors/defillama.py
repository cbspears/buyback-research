#!/usr/bin/env python3
"""DefiLlama data collector — revenue, fees, TVL, holders revenue."""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests

BASE_URL = "https://api.llama.fi"
FEES_URL = "https://fees.llama.fi"

# Map protocol names to DefiLlama slugs
PROTOCOL_SLUGS = {
    "hyperliquid": "hyperliquid",
    "jupiter": "jupiter",
    "ethena": "ethena",
    "jito": "jito",
    "etherfi": "ether.fi",
    "ether.fi": "ether.fi",
    "pump.fun": "pump.fun",
    "pumpfun": "pump.fun",
    "pyth": "pyth-network",
    "pyth-network": "pyth-network",
    "aster": "aster-dex",
    "chainlink": "chainlink",
    "dydx": "dydx",
    "maple": "maple",
    "maple-finance": "maple",
    "clanker": "clanker",
    "raydium": "raydium",
    "uniswap": "uniswap",
    "aave": "aave",
    "makerdao": "makerdao",
    "lido": "lido",
    "banana-gun": "banana-gun",
    "rollbit": "rollbit",
    "metaplex": "metaplex",
    "woo": "woo-network",
}


def get_slug(protocol: str) -> str:
    """Resolve protocol name to DefiLlama slug."""
    key = protocol.lower().strip()
    return PROTOCOL_SLUGS.get(key, key)


def get_protocol_tvl(slug: str) -> dict:
    """Get protocol TVL and basic info."""
    resp = requests.get(f"{BASE_URL}/protocol/{slug}", timeout=30)
    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code}", "slug": slug}

    data = resp.json()
    tvl_history = data.get("tvl", [])
    current_tvl = tvl_history[-1]["totalLiquidityUSD"] if tvl_history else None

    return {
        "name": data.get("name"),
        "slug": slug,
        "category": data.get("category"),
        "chains": data.get("chains", []),
        "current_tvl": current_tvl,
        "tvl_change_7d": data.get("change_7d"),
        "tvl_change_30d": data.get("change_1m"),
        "mcap": data.get("mcap"),
        "symbol": data.get("symbol"),
    }


def get_fees_and_revenue(slug: str) -> dict:
    """Get protocol fees and revenue from DefiLlama fees endpoint."""
    resp = requests.get(f"{FEES_URL}/summary/fees/{slug}", timeout=30)
    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code}", "slug": slug}

    data = resp.json()

    return {
        "name": data.get("name"),
        "slug": slug,
        "total_24h_fees": data.get("total24h"),
        "total_7d_fees": data.get("total7d"),
        "total_30d_fees": data.get("total30d"),
        "total_all_time_fees": data.get("totalAllTime"),
        "total_24h_revenue": data.get("totalRevenue24h"),
        "total_data_chart": data.get("totalDataChart", [])[-30:],  # Last 30 days
    }


def get_revenue_breakdown(slug: str) -> dict:
    """Get detailed revenue data from DefiLlama."""
    resp = requests.get(f"{FEES_URL}/summary/fees/{slug}", timeout=30)
    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code}", "slug": slug}

    data = resp.json()

    # Try to get holders revenue (buyback-relevant)
    holders_revenue = data.get("holdersRevenue24h")

    return {
        "slug": slug,
        "daily_fees": data.get("total24h"),
        "daily_revenue": data.get("totalRevenue24h"),
        "daily_holders_revenue": holders_revenue,
        "protocol_revenue_30d": data.get("total30d"),
    }


def get_holders_revenue_all() -> list:
    """Get all protocols reporting holdersRevenue — indicates active buyback."""
    resp = requests.get(f"{FEES_URL}/overview/fees", timeout=30)
    if resp.status_code != 200:
        return []

    data = resp.json()
    protocols = data.get("protocols", [])

    buyback_protocols = []
    for p in protocols:
        holders_rev = p.get("holdersRevenue24h") or p.get("holdersRevenue30d")
        if holders_rev and holders_rev > 0:
            buyback_protocols.append({
                "name": p.get("name"),
                "slug": p.get("slug") or p.get("defillamaId"),
                "category": p.get("category"),
                "daily_fees": p.get("total24h"),
                "daily_revenue": p.get("totalRevenue24h"),
                "holders_revenue_24h": p.get("holdersRevenue24h"),
                "holders_revenue_30d": p.get("holdersRevenue30d"),
                "chains": p.get("chains", []),
            })

    return sorted(buyback_protocols, key=lambda x: x.get("holders_revenue_24h") or 0, reverse=True)


def collect(protocol: str) -> dict:
    """Collect all DefiLlama data for a protocol."""
    slug = get_slug(protocol)
    print(f"Collecting DefiLlama data for {protocol} (slug: {slug})...")

    tvl_data = get_protocol_tvl(slug)
    fees_data = get_fees_and_revenue(slug)
    revenue_data = get_revenue_breakdown(slug)

    # Estimate annualized figures
    daily_rev = revenue_data.get("daily_revenue") or fees_data.get("total_24h_revenue")
    annual_revenue = daily_rev * 365 if daily_rev else None

    daily_holders = revenue_data.get("daily_holders_revenue")
    annual_holders_revenue = daily_holders * 365 if daily_holders else None

    result = {
        "source": "defillama",
        "protocol": protocol,
        "slug": slug,
        "collected_at": datetime.utcnow().isoformat(),
        "tvl": tvl_data,
        "fees": fees_data,
        "revenue": revenue_data,
        "estimates": {
            "annual_revenue": annual_revenue,
            "annual_holders_revenue": annual_holders_revenue,
        },
    }

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python defillama.py <protocol_name>")
        print("       python defillama.py --scan  (list all protocols with holders revenue)")
        sys.exit(1)

    protocol = sys.argv[1]

    if protocol == "--scan":
        protocols = get_holders_revenue_all()
        result = {
            "source": "defillama_scan",
            "collected_at": datetime.utcnow().isoformat(),
            "protocols_with_buyback": protocols,
            "count": len(protocols),
        }
    else:
        result = collect(protocol)

    # Write to data directory
    data_dir = Path(__file__).parent.parent.parent / "data"
    data_dir.mkdir(exist_ok=True)

    if protocol == "--scan":
        out_path = data_dir / "defillama_scan.json"
    else:
        out_path = data_dir / f"{protocol}_defillama.json"

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)

    print(f"Data written to {out_path}")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
