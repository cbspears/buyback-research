#!/usr/bin/env python3
"""CoinGecko data collector — price, market cap, supply, FDV."""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

BASE_URL = "https://api.coingecko.com/api/v3"

# Map protocol names to CoinGecko IDs
COINGECKO_IDS = {
    "hyperliquid": "hyperliquid",
    "jupiter": "jupiter-exchange-solana",
    "ethena": "ethena",
    "jito": "jito-governance-token",
    "etherfi": "ether-fi",
    "ether.fi": "ether-fi",
    "pump.fun": "pump-fun",
    "pumpfun": "pump-fun",
    "pyth": "pyth-network",
    "pyth-network": "pyth-network",
    "aster": "aster-defi",
    "chainlink": "chainlink",
    "dydx": "dydx-chain",
    "maple": "maple-finance-2",
    "maple-finance": "maple-finance-2",
    "clanker": "clanker",
    "raydium": "raydium",
    "uniswap": "uniswap",
    "berachain": "berachain-bera",
    "eigenlayer": "eigenlayer",
    "arbitrum": "arbitrum",
    "banana-gun": "banana-gun",
    "rollbit": "rollbit-coin",
    "metaplex": "metaplex",
    "woo": "woo-network",
}


def get_headers() -> dict:
    """Get request headers, optionally with API key."""
    headers = {"Accept": "application/json"}
    api_key = os.environ.get("COINGECKO_API_KEY")
    if api_key:
        headers["x-cg-demo-api-key"] = api_key
    return headers


def get_coin_id(protocol: str) -> str:
    """Resolve protocol name to CoinGecko ID."""
    key = protocol.lower().strip()
    return COINGECKO_IDS.get(key, key)


def get_coin_data(coin_id: str) -> dict:
    """Get comprehensive coin data from CoinGecko."""
    resp = requests.get(
        f"{BASE_URL}/coins/{coin_id}",
        params={
            "localization": "false",
            "tickers": "false",
            "market_data": "true",
            "community_data": "false",
            "developer_data": "false",
        },
        headers=get_headers(),
        timeout=30,
    )
    if resp.status_code == 429:
        print("Rate limited by CoinGecko, waiting 60s...")
        time.sleep(60)
        return get_coin_data(coin_id)
    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code}", "coin_id": coin_id}

    data = resp.json()
    md = data.get("market_data", {})

    return {
        "name": data.get("name"),
        "symbol": data.get("symbol", "").upper(),
        "coin_id": coin_id,
        "price_usd": md.get("current_price", {}).get("usd"),
        "market_cap": md.get("market_cap", {}).get("usd"),
        "fully_diluted_valuation": md.get("fully_diluted_valuation", {}).get("usd"),
        "total_volume_24h": md.get("total_volume", {}).get("usd"),
        "circulating_supply": md.get("circulating_supply"),
        "total_supply": md.get("total_supply"),
        "max_supply": md.get("max_supply"),
        "price_change_24h_pct": md.get("price_change_percentage_24h"),
        "price_change_7d_pct": md.get("price_change_percentage_7d"),
        "price_change_30d_pct": md.get("price_change_percentage_30d"),
        "ath": md.get("ath", {}).get("usd"),
        "ath_change_pct": md.get("ath_change_percentage", {}).get("usd"),
        "ath_date": md.get("ath_date", {}).get("usd"),
        "atl": md.get("atl", {}).get("usd"),
        "fdv_to_mcap_ratio": (
            md.get("fully_diluted_valuation", {}).get("usd", 0) /
            md.get("market_cap", {}).get("usd", 1)
            if md.get("market_cap", {}).get("usd")
            else None
        ),
    }


def get_price_history(coin_id: str, days: int = 90) -> list:
    """Get price history for charting."""
    resp = requests.get(
        f"{BASE_URL}/coins/{coin_id}/market_chart",
        params={"vs_currency": "usd", "days": days},
        headers=get_headers(),
        timeout=30,
    )
    if resp.status_code != 200:
        return []

    data = resp.json()
    return [
        {"timestamp": p[0], "price": p[1]}
        for p in data.get("prices", [])
    ]


def collect(protocol: str) -> dict:
    """Collect all CoinGecko data for a protocol."""
    coin_id = get_coin_id(protocol)
    print(f"Collecting CoinGecko data for {protocol} (id: {coin_id})...")

    coin_data = get_coin_data(coin_id)

    # Compute derived metrics
    mcap = coin_data.get("market_cap")
    fdv = coin_data.get("fully_diluted_valuation")
    circ = coin_data.get("circulating_supply")
    total = coin_data.get("total_supply")

    result = {
        "source": "coingecko",
        "protocol": protocol,
        "coin_id": coin_id,
        "collected_at": datetime.utcnow().isoformat(),
        "market_data": coin_data,
        "derived": {
            "fdv_mcap_ratio": fdv / mcap if (fdv and mcap) else None,
            "pct_circulating": circ / total * 100 if (circ and total) else None,
            "dilution_remaining": (total - circ) / total * 100 if (circ and total) else None,
        },
    }

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python coingecko.py <protocol_name>")
        sys.exit(1)

    protocol = sys.argv[1]
    result = collect(protocol)

    data_dir = Path(__file__).parent.parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    out_path = data_dir / f"{protocol}_coingecko.json"

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)

    print(f"Data written to {out_path}")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
